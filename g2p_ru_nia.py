from russian_g2p.Accentor import Accentor
accentor = Accentor()

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
g2p = Grapheme2Phoneme()

import re

with open('/home/lsnoo/nia_russian/nia_data/data_1022/russian_1022.csv', 'r') as f: csv_file = f.readlines()

new_lines = []

for i in csv_file:
	if 'wav' in i: 

		fname = i.split(',')[0]

		## extract sentence
		grapheme = i.split(',')[1].lower()
		#print(grapheme)

		##remove unnecessary symbols
		grapheme = re.sub('[-—=+,;#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', grapheme)
		print(grapheme)

		## make a list of words in the sentence
		grapheme = grapheme.split()
		print(grapheme)
	
		## Utilizing Accentor
		## format for the input of Accentor: [['word1'], ['word2'], ..., ['word_N']]
		word_list = []
		for i in grapheme:
			tmp_word_list = []
			tmp_word_list.append(i)
			word_list.append(tmp_word_list)
		print(word_list)

		#input_accentor = []
		#input_accentor.append(word_list)

		#accented = accentor.do_accents(input_accentor)
		accented = accentor.do_accents(word_list)
		print(accented)

		accented = accented[0]	

		
		##Utilizing Grapheme2Phoneme

		try: 
			phone_list = []
			for i in accented:
				phone = g2p.word_to_phonemes(i)
				phone_list.append(phone)


		## Utilizing g2p
#		phonemes = accented[0]
#		print(phonemes)
#		phoneme_list = g2p.phrase_to_phonemes(phonemes)
#		print(phoneme_list)

			word_phone = []
			for i in phone_list:
				tmp = " ".join(i)
				word_phone.append(tmp)

			phone = " | ".join(word_phone)

			new_line = fname + '\t' + phone + '| \n'
			print(new_line)

			new_lines.append(new_line)

		except:
			new_line = fname + ',' + " ".join(accented) + '\n'
			with open('../nia_data/data_1022/error_sentence_1022.txt', 'a') as f: f.write(new_line)


with open('../nia_data/data_1022/russian_1022_g2p.csv', 'w') as f: f.writelines(new_lines)
