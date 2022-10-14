## NEED to install wget

import json
import wget
import re

audio_save_dir = '/data/lsnoo/nia_ru/audio_1014/'

with open('./data_1014/dataFor12Tagging_1014/ru.json', 'r') as f: entire_dic = json.load(f)

new_lines = []
for dic in entire_dic:
	print(dic)

	
	audio_url = dic["audioUrl"]
	if 'wav' in audio_url:
		wav_file = audio_url.split('/')[-1]
		print(wav_file)
		wav_path = audio_save_dir + wav_file
		print(wav_path)
		# download and save audio_file as "wav_path"
		wget.download(audio_url, wav_path)
	else: wav_path = audio_url

	# extract sentence
	ru_sent = dic["sentence"]
	print(ru_sent)
	ru_sent = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', ru_sent)

	new_line = wav_path + ',' + ru_sent
	print(new_line)

	new_lines.append(new_line)

with open('russian_1014.csv', 'w') as f: f.writelines(new_lines)
