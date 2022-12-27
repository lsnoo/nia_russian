import glob
import soundfile
import re
#from g2pk import G2p
#g2p=G2p()

path_dir = 'data_1022/'
path_csv = path_dir + 'russian_1022_g2p.csv'
with open(path_csv, 'r', encoding='utf-8') as f: lines = f.readlines()

tsv = []
phn = []
wrd = []

for line in lines:
    path = line.split('\t')[0]
    print(path)
    script = line.split('\t')[1]
    print(script)

    num_frame = soundfile.info(path).frames
    tsv_line = path + '\t' + str(num_frame) + '\n'
 
    word = script.replace(' ', '')
    word = word.replace('|', ' ') 
    print(word)
    phone = script
    #phone = phone.replace(' ', '|')
    #phone = ' '.join(phone) 
    print(phone)

    tsv.append(tsv_line)
    phn.append(phone)
    wrd.append(word)

path_save_tsv = path_dir + 'test.tsv'
path_save_phn = path_dir + 'test.phn'
path_save_wrd = path_dir + 'test.wrd'

with open(path_save_tsv, 'w', encoding='utf-8') as f: f.writelines(tsv)
with open(path_save_wrd, 'w', encoding='utf-8') as f: f.writelines(wrd)
with open(path_save_phn, 'w', encoding='utf-8') as f: f.writelines(phn)

#characters = []
#for p in phn:
#    chars = p.split()
#    new_chars = []
#    for i in chars:
#        i += ' 1\n'
#        new_chars.append(i)
#    characters += new_chars

#characters = list(set(characters))
#characters.sort()
#print(characters)

#with open('../40ppl/dict.phn.txt', 'w') as f: f.writelines(characters)

