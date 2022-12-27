from russian_g2p.Accentor import Accentor
accentor = Accentor()

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
g2p = Grapheme2Phoneme()

import re
import json

with open('/home/lsnoo/nia_russian/nia_data/sent_and_target_word/dic_word.json', 'r') as f: dic = json.load(f)
print(dic)

def remove_plus(word):
	word = word.replace('+', '')
	return word

def wrd_to_phoneset(word):
	word = word.lower()
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
		
def sent_to_phoneset(sent):
	##### g2p for a sentence (key)
	sent = sent.lower()
	sent = sent.split()
	##Utilizing Accentor
	##format for the input of Accentor: [['wrd1'], ['wrd2'], ..., ['wrdN']]
	wrd_list = []
	for i in sent:
		tmp_wrd_list = []
		tmp_wrd_list.append(i)
		wrd_list.append(tmp_wrd_list)
	print('wrd_list_key: ', wrd_list)

	accented = accentor.do_accents(wrd_list)    ### accented = ['aply', 'apple']
	print('accented_key: ', accented)

	try:
		phone_list = []
		for j in accented:
			phone = g2p.word_to_phonemes(j)
			print('phone_key: ', phone)
			phone_list.append(phone)    ### output: [['a', 'p', 'l', 'ai', ...], ['f', 'l', ai']]
		print('phone_list: ', phone_list)

		wrd_phone = []
		for p in phone_list:      ### p = ['f', 'l', 'ai']
			tmp = ' '.join(p)       ### tmp: 'f l ai'
			print('tmp_wrd_phone_key: ', tmp)
			wrd_phone.append(tmp)      ### output: wrd_phone = ['f l ai', 'a p l ai']

		phone = " ".join(wrd_phone) ### phone = 'f l ai a p l ai' 
		print('key_phone: ', phone)

		return phone

	except: 
		phone_list = []
		accented = list(map(remove_plus, accented[0]))
		for j in accented:
			print('except_j: ', j)
			#j = j[0].replace('+', '')
			phone = g2p.word_to_phonemes(j)
			print('except_phone: ', phone)
			phone_list.append(phone)
			print('except_phone_list: ', phone_list)

		wrd_phone = []
		for p in phone_list:
			tmp = ' '.join(p) 
			print('except_tmp: ', tmp)
			wrd_phone.append(tmp)

		phone = ' '.join(wrd_phone)
		print('except_phone: ', phone)

		return phone



for k, v in dic.items():
	new_k = sent_to_phoneset(k)
	print('new_k: ', new_k)
	
	dic[new_k] = dic.pop(k)

	## change value of the key
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
		
	dic[new_k] = new_value
	print(new_k, dic[new_k])
	

with open('../nia_data/sent_and_target_word/dic_word_g2p.json', 'w') as f: json.dump(dic, f, indent=4)
