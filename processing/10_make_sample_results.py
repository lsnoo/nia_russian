import re
import json

with open('./data_1114/results/per_utt_results', 'r', encoding='utf-8') as f: results = f.readlines()
with open('./data_1114/russian_1114_without_error.csv', 'r', encoding='utf-8') as f: csv_lines = f.readlines()

new_results ={}

def cleaning(sent):
	new_sent = re.sub(r'\s+', ' ', sent)
	new_sent = new_sent.split(' ')
	new_sent = ' '.join(new_sent[2:])
	return new_sent

len_result = len(csv_lines)

for num in range(len_result):

	ref_idx = (num*4)
	hyp_idx = (num*4) + 1
	err_idx = (num*4) + 2
	ptr_idx = (num*4) + 3

	wav_file = csv_lines[num].split(',')[0].split('/')[-1]
	print('wav_file: ', wav_file)
	russian_text = csv_lines[num].split(',')[1]
	russian_text = russian_text.replace('\n', '')
	russian_text = russian_text.strip()
	print('russian: ', russian_text)

	canonical_phn = results[ref_idx]
	print(canonical_phn)
	canonical_phn = cleaning(canonical_phn)
	print('canonical phone: ', canonical_phn)

	recognized_phn = results[hyp_idx]
	print(recognized_phn)
	recognized_phn = cleaning(recognized_phn)
	print('recognized_ phone: ', recognized_phn)

	error_per_phone = results[err_idx]
	print(error_per_phone)
	error_per_phone = cleaning(error_per_phone)
	print('error per phone: ', error_per_phone)

	num_error = results[ptr_idx]
	num_error = cleaning(num_error)

	letters = error_per_phone.replace(' ', '')
	num_phn = len(letters)
	num_cor = letters.count('C')
	per = 1 - (num_cor/num_phn)



	wav_dic = {}
	wav_dic['fName'] = wav_file
	wav_dic['transSpell'] = russian_text
	wav_dic['transAnsw'] = canonical_phn
	wav_dic['transWrong'] = recognized_phn
	wav_dic['per'] = per
	wav_dic['error_pattern'] = error_per_phone
	wav_dic['#ofCSID'] = num_error
	print(wav_dic)

	new_results[num] = wav_dic
	#new_results.append(wav_dic)

with open('./data_1114/Results_Russian_221121.json', 'w', encoding='utf-8') as f: json.dump(new_results, f, indent=4, ensure_ascii=False)
print(new_results)
