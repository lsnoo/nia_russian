with open('./data_1114/error_path.txt', 'r') as f: path = f.readlines()
with open('./data_1114/error_sentence_1114.txt', 'r') as f: error_sents = f.readlines()
with open('./data_1114/russian_1114.csv', 'r') as f: csv_sents = f.readlines()

new_path = []

for i in path:
	i = i.replace('\n', '').split('/')[-1]
	print(i)
	new_path.append(i)

new_sents = []
for sent in csv_sents:
	wav_path = sent.split(',')[0].split('/')[-1]
	#lower_sent = script.lower()
	#lower_sent = sent.split(',')[0] + ',' + lower_sent
	if wav_path in new_path:
		new_sent = wav_path + ',' + sent.split(',')[1]
		print(new_sent)
		new_sents.append(new_sent)

with open('./data_1114/russian_1114_without_error.csv', 'w') as f: f.writelines(new_sents)
