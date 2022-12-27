from russian_g2p.Accentor import Accentor
accentor = Accentor()

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
g2p = Grapheme2Phoneme()

import re
import json

with open('/home/lsnoo/nia_russian/nia_data/sent_and_target_word/dic_word.json', 'r') as f: dic = json.load(f)
print(dic)

def wrd_to_phoneset(word):
	wrd_in_list = [[word]]
	print('wrd_in_list: ', wrd_in_list)
	accented_wrd_list = accentor.do_accents(wrd_in_list)
	accented_wrd = accented_wrd_list[0][0]

	try: 
		phone_list = g2p.word_to_phonemes(accented_wrd)
		phone_line = " ".join(phone_list)
		return phone_line

	except:
		new_line = word + '\t' + " ".join(accented_wrd) + '\n'
		with open('../nia_data/sent_and_target_word/error_sentence_g2p.txt', 'a') as f: f.write(new_line)
		return 'G2P_ERROR'
		

for k, v in dic.items():
	print(v)
	new_value = []

	for j in v:
		print("print j: ",j)
		wrd_list = j.lower().split(' ')
		
		new_string = ''
		for wrd in wrd_list:
			phn_string = wrd_to_phoneset(wrd)
			new_string += phn_string

		new_value.append(new_string)
		
	dic[k] = new_value
	print(k, dic[k])
	

with open('../nia_data/sent_and_target_word/dic_word_g2p.json', 'w') as f: json.dump(dic, f, indent=4)
