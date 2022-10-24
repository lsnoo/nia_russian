import re
from collections import Counter
import json

with open('/home/lsnoo/nia_russian/nia_data/data_1014/results/per_utt_results_1014', 'r') as f: lines = f.readlines()

num_utt = int(len(lines)/4)


errors = []
for num in range(num_utt):

	ref_idx = (num*4)
	hyp_idx = (num*4) + 1
	err_idx = (num*4) + 2

	ref = lines[ref_idx]
	hyp = lines[hyp_idx]
	err = lines[err_idx]

	ref = re.sub(r'\s+', ' ', ref)
	hyp = re.sub(r'\s+', ' ', hyp)
	err = re.sub(r'\s+', ' ', err)
	print('single_space: ref', ref, '\nhyp: ', hyp, '\nerr', err)
	

	ref = ref.split(' ')[2:]
	hyp = hyp.split(' ')[2:]
	err = err.split(' ')[2:]

	for j in range(len(ref)):
		if ref[j] == hyp[j]: pass
		else:
			if '*' in  hyp[j]: 
				result = "deletion of " + "< " + ref[j] + " >"
				print(result)
				errors.append(result)
			elif '*' in ref[j]: 
				result = "insertion of " + "< " + hyp[j] + " >"
				print(result)
				errors.append(result)
			else: 
				result = "substitute of " + "< " + ref[j] + " > to < " + hyp[j] + " >"
				print(result)
				errors.append(result)



## Count the number of each error pattern
error_dic = Counter(errors)

with open('/home/lsnoo/nia_russian/nia_data/data_1014/results/error_patterns_dic', 'w') as f: json.dump(error_dic, f, indent=4)
print(error_dic)

sorted_tuple = sorted(error_dic.items(), key = lambda item: item[1], reverse = True)
print(sorted_tuple[:50])
with open('/home/lsnoo/nia_russian/nia_data/data_1014/results/error_patterns_dic_50', 'w') as f: f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in sorted_tuple))
