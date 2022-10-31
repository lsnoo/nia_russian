#with open('./data_1014/results/hypo.units-checkpoint_best.pt-test.txt', 'r') as f1:
with open('./data_1014/dic_word_g2p.json', 'r') as f1:
    sents = f1.readlines()

IPAdic = {
        'U0': 'ˈu',  # close back/front rounded vowel with stress?
		'U': 'u', # without stress
        'O0': 'ˈo',  # close-mid back rounded vowel
        'A0': 'ˈa',  # open front unrounded vowel with stress
        'A': 'a', # without stress
        'E0': 'ˈe',  # close-mid/open-mid front unrounded vowel
        'Y0': 'ˈɨ',  # close central unrounded vowel with stress
        'Y': 'ɨ',  # without stress
        'I0': 'ˈi', # close front unrounded vowel - with stress?
        'I': 'i',  # without stress?
        'K0': 'kʲ',  
        'KH0': 'xʲ', 
        'KH': 'x', # voiceless velar fricative
        'K': 'k', # voiceless velar stop
        'GH0': 'ɣʲ', 
        'GH': 'ɣ', # voiced velar fricative
        'G0': 'gʲ', 
        'G': 'g', # voiced velar stop
        'J0': 'j', # palatal approximant
		'TSH0': 'tɕ', 
        'TSH': 'tʂ', # voiceless alveolo-palatal affricate
        'SH0': 'ɕː', 
        'SH': 'ʂ', # voiceless retroflex fricative
        'ZH0': 'ʑː', 
        'ZH': 'ʐ', # voiced retroflex fricative
        'DZ0': 'dzʲ', 
        'DZ': 'dz', # voiced alveolar affricate
        'DZH0': 'dʑhʲ', 
        'DZH': 'dʑh', # voiced alveolo-palatal affricate
        'R0': 'rʲ', 
        'R': 'r', # alveolar and postalveolar trills
        'T0': 'tʲ', 
        'T': 't', # voiceless dental stop
        'TS0': 'tsʲ', 
        'TS': 'ts', # voiceless alveolar affricate
        'S0': 'sʲ', 
        'S': 's', # voiceless alveolar sibilant
        'D0': 'dʲ', 
        'D': 'd', # voiced dental stop
        'Z0': 'zʲ', 
        'Z': 'z', # voiced alveolar fricative
        'N0': 'nʲ',  
        'N': 'n', # alveolar nasal
        'L0': 'lʲ', 
        'L': 'ɬ',  # velarized alveolar lateral approximant
		'P0': 'pʲ', 
        'P': 'p',  # voiceless bilabial stop
		'F0': 'fʲ', 
		'F': 'f',  # voiceless labiodental fricative
		'B0': 'bʲ', # voiced bilabial stop
		'B': 'b',
		'V0': 'vʲ', 
		'V': 'v', # voiced labiodental fricative
		'M0': 'mʲ',
		'M': 'm' # bilabial nasal
        }

def toIPA(string):
    for key in IPAdic:
        string = string.replace(key, IPAdic[key])
    return string

import re

newsents = []
for sent in sents:
	#idx = re.search('\(', sent).start()
	
	#file_num = sent[idx:-1]
	#plu_sent = sent[:idx] 
	
	ipa_sent = toIPA(sent)
	
	#new_line = file_num + '\t' + ipa_sent + '\n'

	newsents.append(ipa_sent)

with open('./data_1014/dic_word_g2p_ipa.json', 'w') as f2:
    f2.writelines(newsents)

