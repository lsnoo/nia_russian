#!/bin/bash

outputdir='/converted_1014'
mkdir -p $outputdir

for file in audio_1014/*.wav
do
	filename=$(basename $file)
	outputfile="${outputdir}/${file}"
	mkdir -p $(dirname $outputfile)

	sox $file -r 16k -b 16 -c 1 $outputfile
done
