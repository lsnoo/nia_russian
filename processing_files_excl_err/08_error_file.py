with open('./data_1114/test.tsv', 'r') as f: lines = f.readlines()

new_line = []

for i in lines:
	if 'wav' in i:
		path = i.split('\t')[0] + '\n' 
		new_line.append(path)

with open('./data_1114/error_path.txt', 'w') as f: f.writelines(new_line)
