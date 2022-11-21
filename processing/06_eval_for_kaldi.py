from jiwer import wer

with open('./data_1114/results/hypo.units-checkpoint_best.pt-test.txt_ipa', 'r', encoding='utf-8') as f1: hypo = f1.readlines()
#print(hypo)
with open('./data_1114/results/ref.units-checkpoint_best.pt-test.txt_ipa', 'r', encoding='utf-8') as f2: ref = f2.readlines()
#print(ref)

def cleaning(sent):
		
	#	sent = sent.split('\t')[1].replace("| ", "").replace('\n', '')
	#sent = sent.split('\t')[1].replace("| ", "")
	sent = sent.replace("| ", "").replace("\n", "") + '\n'
	print(sent)
	return sent
			
	#new_sents = []
	#for linei in sents:
	#		print(linei)
	#		linei = linei.split('\t')[1] 
	#		print(linei)
	#		linei= linei.replace("| ", "")
	#		print(linei)
	#		new_sents.append(linei)
	#	return new_sents
		#sent = sent.split('\t')[-1]
		#print(sent)
		#sents[i] = sent.replace("| ", "")
		#print(sents[i])

ground_truth = list(map(cleaning, ref))
hypothesis = list(map(cleaning, hypo))


with open('./data_1114/results/hyp', 'w') as f: f.writelines(hypothesis)
with open('./data_1114/results/ref', 'w') as f: f.writelines(ground_truth)

#error = wer(ground_truth, hypothesis)

#print(error)
