import re
import json

with open('/home/lsnoo/nia_russian/nia_data/data_1014/results/per_utt_results_1014_tab', 'r') as f1: results = f1.readlines()

with open('/home/lsnoo/nia_russian/nia_data/sent_and_target_word/dic_word_g2p_ipa.json', 'r') as f2: target_dic = json.load(f)


