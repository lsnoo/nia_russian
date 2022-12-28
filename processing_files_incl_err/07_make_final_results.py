import re
import json

with open('./data_1220/results/per_utt_results', 'r', encoding='utf-8') as f: resultss = f.readlines()
with open('./data_1220/russian_1220_g2p.csv', 'r', encoding='utf-8') as f: csv_lines = f.readlines()
with open('./data_1220/original_json/ru.json', 'r') as f: ru_json = json.load(f)

new_resultss ={}

def cleaning(sent):
	new_sent = re.sub(r'\s+', ' ', sent)
	new_sent = new_sent.split(' ')
	new_sent = ' '.join(new_sent[2:])
	return new_sent

len_results = len(csv_lines)

#wav_file_results = []

recog_ipa = []
canon_ipa = []
tagging_list = []
for num in range(len_results):

	ref_idx = (num*4)
	hyp_idx = (num*4) + 1
	err_idx = (num*4) + 2
	ptr_idx = (num*4) + 3

	#wav_file = csv_lines[num].split(',')[0].split('/')[-1]
	#print('wav_file: ', wav_file)
	#wav_file_results.append(wav_file)
	#russian_text = csv_lines[num].split(',')[1]
	#russian_text = russian_text.replace('\n', '')
	#russian_text = russian_text.strip()
	#print('russian: ', russian_text)

	canonical_phn = resultss[ref_idx]
	print(canonical_phn)
	canonical_phn = cleaning(canonical_phn)
	canon_ipa.append(canonical_phn)
	print('canonical phone: ', canonical_phn)

	recognized_phn = resultss[hyp_idx]
	print(recognized_phn)
	recognized_phn = cleaning(recognized_phn)
	recog_ipa.append(recognized_phn)
	print('recognized_ phone: ', recognized_phn)

	error_per_phone = resultss[err_idx]
	print(error_per_phone)
	error_per_phone = cleaning(error_per_phone)
	tagging_list.append(error_per_phone)
	print('error per phone: ', error_per_phone)


results_list = []

for i in range(len(ru_json)):
	temp_dic = {}
	temp_dic["project_id"] = ru_json[i]["projectId"]
	temp_dic["document_id"] = ru_json[i]["documentId"]
	temp_dic["section_id"] = ru_json[i]["sectionId"]
	temp_dic["segment_id"] = ru_json[i]["segmentId"]
	temp_dic["index"] = ru_json[i]["index"]
	temp_dic["lang"] = ru_json[i]["lang"]
	temp_dic["sentence"] = ru_json[i]["sentence"]
	temp_dic["audioUrl"] = ru_json[i]["audioUrl"]
	temp_dic["warning"] = ""
	temp_dic["tagging"] = {}

	#wav_name = ru_json[i]["audioUrl"].split('/')[-1]
	
	#idx_results = wav_file_results.index(wav_name)
	
	if '** <unk> <unk>' not in canon_ipa[i]:
	#if wav_name in wav_file_results:
		temp_dic["tagging"]["transAnsw"] = canon_ipa[i][:-1]
		temp_dic["tagging"]["phonemeText"] = recog_ipa[i][:-1]
		temp_dic["tagging"]["tagging"] = tagging_list[i][:-1]

	else: 
		temp_dic["warning"] = "G2P error!"
		temp_dic["tagging"]["transAnsw"] = ""
		temp_dic["tagging"]["phonemeText"] = recog_ipa[i][:-1]
		temp_dic["tagging"]["tagging"] = ""
	
	results_list.append(temp_dic)



with open('./data_1220/final_ru.json', 'w', encoding='utf-8') as f: json.dump(results_list, f, indent=4, ensure_ascii=False)
