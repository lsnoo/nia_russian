import json

with open('data_1220/old_form.json', 'r') as f: result_data = json.load(f)
with open('data_1220/ru.json', 'r') as f: ru_json=json.load(f)

wav_file_result = []
for i in result_data:
	#print(i)
	#print(type(i))
	new_line = result_data[i]["fName"]
	#print(new_line)
	wav_file_result.append(new_line)

for i in range(len(ru_json)):
	wav_name = ru_json[i]["audioUrl"].split('/')[-1]
	ru_json[i]["warning"] = ""
	
	if wav_name in wav_file_result:
		idx_result = str(wav_file_result.index(wav_name))
		#target_dic = result_data[idx_result]

		#tagging_list = []
		tagging_dic = {}
		tagging_dic["transAnsw"] = result_data[idx_result]["transAnsw"]
		tagging_dic["phonemeText"] = result_data[idx_result]["transWrong"]
		tagging_dic["tagging"] = result_data[idx_result]["error_pattern"]
		#tagging_list.append(tagging_dic)
		print(tagging_dic)

		ru_json[i]["tagging"] = tagging_dic

	else: 
		ru_json[i]["warning"] = "G2P Error"
		
		tagging_dic = {}
		tagging_dic["transAnsw"] = ""
		tagging_dic["phonemeText"] = ""
		tagging_dic["tagging"] = ""
		
		ru_json[i]["tagging"] = tagging_dic


with open('data_1220/ru_1220.json', 'w') as f: json.dump(ru_json, f, indent=4, ensure_ascii=False)
