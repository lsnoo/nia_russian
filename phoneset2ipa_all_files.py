import re

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


def change_to_IPA(sent):
    idx = re.search('\(', sent).start()
    file_num = sent[idx:-1]
    file_num = file_num.replace('(None-', '')
    file_num = file_num.replace(')', '').zfill(5)

    plu_sent = sent[:idx].upper() 
    ipa_sent = toIPA(plu_sent)
    new_sent = file_num + '\t' + ipa_sent + '\n'
    print(new_sent)
    return new_sent

def applying(path_dir, unit):
    common_part = '-checkpoint_best.pt-test.txt'
    fname_hypo = path_dir + 'hypo.' + unit + common_part
    fname_ref = path_dir + 'ref.' + unit + common_part
    
    with open(fname_hypo, 'r') as f: sents_hypo = f.readlines()
    sents_hypo = list(map(change_to_IPA, sents_hypo))
    sents_hypo.sort()
    with open(fname_ref, 'r') as f: sents_ref = f.readlines()
    sents_ref = list(map(change_to_IPA, sents_ref))
    sents_ref.sort()

    print(sents_ref[:3])
    new_fname_hypo = fname_hypo + '_ipa'
    new_fname_ref = fname_ref + '_ipa'
    
    with open(new_fname_ref, 'w') as f: f.writelines(sents_ref)
    with open(new_fname_hypo, 'w') as f: f.writelines(sents_hypo)


path_dir = './data_1014/results/'
unit = ['units', 'word']

for i in unit: applying(path_dir, i)
