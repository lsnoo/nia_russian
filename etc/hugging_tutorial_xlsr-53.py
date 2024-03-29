##### Prepare Data, Tokenizer, Feature Extractor
### Create Tokenizer
print('===========================Create Wav2Vec2CTCTokenizer=====================')

from datasets import load_dataset, load_metric, Audio

common_voice_train = load_dataset("common_voice", 'ru', split="train+validation")
common_voice_test = load_dataset("common_voice", "ru", split="test")

common_voice_train = common_voice_train.remove_columns(["accent", "age", "client_id", "down_votes", "gender", "locale", "segment", "up_votes"])
common_voice_test = common_voice_test.remove_columns(["accent", "age", "client_id", "down_votes", "gender", "locale", "segment", "up_votes"])


# Data pre-processing
from datasets import ClassLabel
import random
import pandas as pd
#from IPython.display import display, HTML

#def show_random_elements(dataset, num_examples=10):
#	assert num_examples <= len(dataset), "Can't pick more elements than there are in the dataset."
#	picks = []
#	for _ in range(num_examples):
#		pick=random.randint(0, len(dataset)-1)
#		while pick in picks:
#			pick = random.randint(0,len(dataset)-1)
#		picks.append(pick)
	
#	df = pd.DataFrame(dataset[picks])
#	display(HTML(df.to_html()))

#show_random_elements(common_voice_train.remove_columns(["path", "audio"]), num_examples=10)

# Cleaning the sentence
import re
chars_to_remove_regex = '[\,\?\.\!\-\;\:\"\“\%\‘\”\�\';-–—]'

def remove_special_characters(batch):
	batch['sentence'] = re.sub(chars_to_remove_regex, '', batch['sentence']).lower()
	return batch

common_voice_train = common_voice_train.map(remove_special_characters)
common_voice_test = common_voice_test.map(remove_special_characters)

# making vocab
def extract_all_chars(batch):
	all_text = " ".join(batch['sentence'])
	vocab = list(set(all_text))
	return {"vocab": [vocab], "all_text": [all_text]}

vocab_train = common_voice_train.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_train.column_names)
vocab_test = common_voice_test.map(extract_all_chars, batched=True, batch_size=-1, keep_in_memory=True, remove_columns=common_voice_test.column_names)

vocab_list = list(set(vocab_train['vocab'][0]) | set(vocab_test["vocab"][0]))

vocab_dict = {v: k for k, v in enumerate(sorted(vocab_list))}
print(vocab_dict)

vocab_dict["|"] = vocab_dict[" "]
del vocab_dict[" "]
print("length of vocab_dict: ", len(vocab_dict))

vocab_dict["[UNK]"] = len(vocab_dict)
vocab_dict["[PAD]"] = len(vocab_dict)
print("length of vocab_dict: ", len(vocab_dict))

# saving vocabulary as a json file
import json
with open('vocab.json', 'w') as vocab_file: json.dump(vocab_dict, vocab_file)

# using the json file to load the  vocabulary into an instance of the tokenizer class
from transformers import Wav2Vec2CTCTokenizer

tokenizer = Wav2Vec2CTCTokenizer.from_pretrained("./", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")

repo_name="wav2vec2-large-xlsr-53k-russian"

tokenizer.push_to_hub(repo_name)

### CREATE Wav2Vec2FeatureExtractor
print('===========================Create Wav2Vec2FeatureExtractor=====================')

from transformers import Wav2Vec2FeatureExtractor
feature_extractor = Wav2Vec2FeatureExtractor(feature_sieze=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)

from transformers import Wav2Vec2Processor
processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)


### Preprocess Data
print('===========================Process Data=====================')

common_voice_train = common_voice_train.cast_colum("audio", Audio(sampling_rate=16_000))
common_voice_test = common_voice_test.cast_column("audio", Audio(sampling_rate=16_000))

def prepare_dataset(batch):
	audio = batch["audio"]
	batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
	batch["input_length"] = len(batch["input_values"])

	with processor.as_target_processor():
		batch["labels"] = processor(batch["sentence"]).input_ids
	return batch

common_voice_train = common_voice_train.map(prepare_dataset, remove_columns=common_voice_train.column_names)
common_voice_test = common_voice_test.map(prepare_dataset, remove_columns=common_voice_test.column_names)

##### Training
print('===========================***Training***===============================')

### setting up Trainer
print('===========================Set-up Trainer=====================')

import torch
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
	Args:
        processor (:class:`~transformers.Wav2Vec2Processor`)
		    The processor used for proccessing the data.
	    padding (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.PaddingStrategy`, `optional`, defaults to :obj:`True`):
		    Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
		    among:
		    * :obj:`True` or :obj:`'longest'`: Pad to the longest sequence in the batch (or no padding if only a single sequence if provided).
   		    * :obj:`'max_length'`: Pad to a maximum length specified with the argument :obj:`max_length` or to the maximum acceptable input length for the model if that argument is not provided.
        	* :obj:`False` or :obj:`'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of different lengths).
	"""
	processor: Wav2Vec2Processor
	padding: Union[bool, str] = True

	def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
		# split inputs and labels since they have to be of different lengths and need different padding methods
		input_features = [{"input_values": feature["input_values"]} for feature in features]
		label_features = [{"input_ids": feature["labels"]} for feature in features]

		batch = self.processor.pad(
				input_features,
				padding=self.padding,
				return_tensors="pt",
		)
		with self.processor.as_target_processor():
			labels_batch = self.processor.pad(
					label_features,
					padding=self.padding,
					return_tensors="pt",
			)

		# replace padding with -100 to ignore loss correctly
		labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

		batch["labels"] = labels

		return batch


data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)


## METRIC
wer_metric = load_metric("wer")

def compute_metrics(pred):
	pred_logits = pred.predictions
	pred_ids = np.argmax(pred_logits, axis=-1)

	pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

	pred_str = processor.batch_decode(pred_ids)
	#we do not want to group tokens when computing the metrics
	label_str = processor.batch_decode(pred.label_ids, group_tokens=False)

	wer = wer_metric.compute(predictions=pred_str, references=label_str)

	return {"wer": wer}


### Loading the pretrained model
print("==========================Loading the pretrained model======================")
from transformers import Wav2Vec2ForCTC

model = Wav2Vec2ForCTC.from_pretrained(
		"facebook/wav2vec2-large-xlsr-53",
		attention_dropout=0.0,
		hidden_dropout=0.0,
		mask_time_prob=0.05,
		layerdrop=0.0,
		ctc_loss_reduction="mean",
		pad_token_id=processor.tokenizer.pad_token_id,
		vocab_size=len(processor.tokenizer)
		)

model.freeze_feature_extractor()

### Setting Training Arguments
print("========================Training Arguments===========================")

from transformers import TrainingArguments
training_args = TrainingArguments(
		output_dir=repo_name,
		group_by_length=True,
		per_device_train_batch_size=16,
		gradient_accumulation_steps=2,
		evaluation_strategy="steps",
		num_train_epochs=30,
		gradient_checkpointing=True,
		fp16=True,
		save_steps=400,
		eval_steps=400,
		logging_steps=400,
		learning_rate=3e-4,
		warmup_steps=500,
		save_total_limit=2,
		push_to_hub=True,
	)

### Setting up Trainer
print('====================Trainer=======================')

from transformers import Trainer

trainer = Trainer(
		model=model,
		data_collator=data_collator,
		args=training_args,
		compute_metrics=compute_metrics,
		train_dataset=common_voice_train,
		test_dataset=common_voice_test,
		tokenizer=processor.feature_extractor,
	)

### TRAINING
print('-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=-=-=-=-=-=TRAINING=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

trainer.train()

trainer.push_to_hub()


##### EVALUATION
print('========================================EVALUATION=========================================')

model = Wav2Vec2ForCTC.from_pretrained(repo_name).to("cuda")
processor = Wav2Vec2Processor.from_pretrained(repo_name)


input_dict = processor(common_voice_test[0]["input_values"], return_tensors="pt", padding=True)
logits = model(input_dict.input_values.to("cuda")).logits
pred_ids = torch.argmax(logits, dim=-1)[0]

common_voice_test_transcription = load_dataset("common_voice", "ru", data_dir='./common_voice_dataset_ru', split="test")

print("prediction:")
print(processor.decode(pred_ids))

print('\nReference:')
print(common_voice_test_transcription[0]["sentence"].lower())


