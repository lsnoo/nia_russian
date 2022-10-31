#!/bin/bash

# find all .pcm files and convert them to wav

for input_file in `find /home/lsnoo/nia_russian/nia_data/data/lsnoo/ksponspeech/ksponspeech01/KsponSpeech_01/KsponSpeech_0123/*.pcm`
do
#	echo $input_file
	output_file=`echo $input_file | sed 's/\//-/g' | sed 's/pcm/wav/g' | sed 's/-data-lsnoo-ksponspeech-ksponspeech01-KsponSpeech_01-//g'`
	echo $output_file
#	ffmpeg -v quiet -f s16le -ar 16k -ac 1 -i $input_file $output_file
	ffmpeg -f s16le -ar 16k -ac 1 -i $input_file $output_file
done
