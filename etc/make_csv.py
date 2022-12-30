import json
import wget
import re

audio_save_dir = '/data/lsnoo/nia_ru/audio_1014/'

with open('./data_1014/dataFor12Tagging_1014/ru.json', 'r') as f: entire_dic = json.load(f)

#print(len(entire_dic))
#entire_dic = entire_dic[0].replace(',{', ', {')
#entire_dic = entire_dic.replace(":", ": ")
#entire_dic = entire_dic.replace(',"', ', "')
#entire_dic = list(entire_dic)
#with open('revised.json', 'w') as f: f.writelines(entire_dic)
#print(len(entire_dic))
#print(type(entire_dic[0]))

new_lines = []
for dic in entire_dic:
	print(dic)
	
	audio_url = dic["audioUrl"]
	wav_file = audio_url.split('/')[-1]
	print(wav_file)
	wav_path = audio_save_dir + wav_file
	print(wav_path)
	# download and save audio_file as "wav_path"
	wget.download(audio_url, wav_path)

	# extract sentence
	ru_sent = dic["sentence"]
	print(ru_sent)
	ru_sent = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', '', ru_sent)

	new_line = wav_path + ',' + ru_sent
	print(new_line)

	new_lines.append(new_line)

with open('russian_1014.csv', 'w') as f: f.writelines(new_lines)