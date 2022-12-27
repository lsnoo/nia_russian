import glob
import librosa


#flist = glob.glob('data_1014/converted_1014/audio_1014/*.wav')

with open('./data_1022/russian_1022.csv', 'r') as f: lines = f.readlines()

flist = []
for i in lines:
	i = i.split(',')[0]
	flist.append(i)

seconds = 0

for i in flist:
    f_dur = librosa.get_duration(filename = i)
    seconds += f_dur

hours = round(seconds//3600)
mins = round((seconds%3600)//60)
secs = round(seconds%60)

duration_hms = str(hours) + ':' + str(mins) + ':' + str(secs)

print('number of files: ' + str(len(flist)))
print('total_seconds: ' + str(round(seconds)))
print('H:M:S = ' + duration_hms)

