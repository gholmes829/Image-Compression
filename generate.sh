#!/bin/bash

# Generates compressed images
# Usage ./gen.sh file alg start stop step overflow log
# See ./__main__ usage for more details

FILE=$1
alg=$2
mode=$3

curr=$4
stop=$(($5 + 1))
step=$6

protectOverflow=$7

log=$8

name=${FILE%%.*}
ext=${FILE##*.}

directory=${name}\_${alg}\_${mode}\_${protectOverflow}

endl=$'\n'

mkdir -p ./output/$directory

echo "GENERATING IMAGES:${endl}"

while [ $curr -lt $stop ]
do
    echo "Running iteration: Value = ${curr}"
	output=${name}\_${curr}.$ext
	path=${directory}/${output}

	if [[ !( -f "output/${path}") ]]
	then
		echo ${endl}
    	./__main__.py $FILE $alg $mode $curr $protectOverflow $log $path
		echo "${endl}Done.${endl}${endl}${endl}"
	else
	 echo "${output} already exists, skipping iteration...${endl}"
	fi
    curr=$(($curr + $step))

done

echo "SCRIPT COMPLETED"

