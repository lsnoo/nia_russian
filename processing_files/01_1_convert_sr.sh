#!/bin/bash

outputdir='/converted_1220'
mkdir -p $outputdir

for file in data_1220/*.wav
do
	filename=$(basename $file)
	outputfile="${outputdir}/${file}"
	mkdir -p $(dirname $outputfile)

	sox $file -r 16k -b 16 -c 1 $outputfile
done
