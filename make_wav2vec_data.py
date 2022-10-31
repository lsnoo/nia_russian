import soundfile as sf
import re

with open('/home/lsnoo/nia_russian/wav2vec_data/dev_audio.txt', 'r') as f: lines = f.readlines()

tsv_list = []
phn_list = []
wrd_list = []
dict_list = []

for line in lines:
	fname = line.split('\t')[0]
	sent = line.split('\t')[1]

	length = sf.info(fname).frames

	tsv_line = fname + '\t' + str(length) + '\n'

	phn_line = sent[:-1] +  '|\n'

	wrd_line = phn_line.replace(" ", "")
	wrd_line = wrd_line.replace("|", " ")

	phns = sent[:-1]
	phns = phns.replace(" |", "")
	phns = phns.split(" ")
	dic_list = []
	for phn in phns:
		dict_line = phn + ' 1\n'
		#print('DICT_LINE: ', dict_line)
		if dict_line in dic_list: pass
		else: dic_list.append(dict_line)

	print(tsv_line)
	print(phn_line)
	print(wrd_line)
	#print(dic_list)

	tsv_list.append(tsv_line)
	phn_list.append(phn_line)
	wrd_list.append(wrd_line)
	dict_list.extend(dic_list)

dict_list = list(set(dict_list))
dict_list.sort()
print('DICT: ', dict_list)


with open('/home/lsnoo/nia_russian/wav2vec_data/dev.tsv', 'w') as f: f.writelines(tsv_list)
with open('/home/lsnoo/nia_russian/wav2vec_data/dev.phn', 'w') as f: f.writelines(phn_list)
with open('/home/lsnoo/nia_russian/wav2vec_data/dev.wrd', 'w') as f: f.writelines(wrd_list)
#with open('/home/lsnoo/nia_russian/wav2vec_data/dict.phn.txt', 'w') as f: f.writelines(dict_list)
