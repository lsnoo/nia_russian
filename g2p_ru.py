### should be run in the "../russian_g2p" directory... USE the file "g2p_ru_nia.py"
from russian_g2p.Accentor import Accentor
accentor = Accentor()

from russian_g2p.Grapheme2Phoneme import Grapheme2Phoneme
g2p = Grapheme2Phoneme()

import re

with open('data_014/russian_1014.csv', 'r') as f: csv_file = f.readlines()

new_lines = []

for i in csv_file:

	fname = i.split(',')[0]

	## extract sentence
	grapheme = i.split(',')[1]
	#print(grapheme)

	##remove unnecessary symbols
	grapheme = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', grapheme)
	print(grapheme)

	## make a list of words in the sentence
	grapheme = grapheme.split()

	## Utilizing Accentor
	## format for the input of Accentor: [['word1'], ['word2'], ..., ['word_N']]
	word_list = []
	for i in grapheme:
		word_list.append(i)
	
	input_accentor = []
	input_accentor.append(word_list)

	accented = accentor.do_accents(input_accentor)


	## Utilizing g2p
	accented = " ".join(accented[0])
	print(accented)

	phoneme = g2p.phrase_to_phonemes(accented)
	print(phoneme)

	new_line = fname + '\t' + phoneme + '\n'

	new_lines.append(new_line)

with open('data_1014/russian_1014_g2p.csv', 'w') as f: f.writelines(new_lines)
