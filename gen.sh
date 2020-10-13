#!/bin/sh

#generates compressed images
#usage ./gen.sh file alg start stop step

start=$3
finish=$(($4 + 1))
step=$5

FILE=$1

name=${FILE%%.*}
ext=${FILE##*.}

alg=$2

directory=${name}\_$alg

mkdir -p ./output/$directory

while [ $start -lt $finish ]
do
    echo Running for \#components = ${start}
    ./__main__.py $FILE $alg c $start ${directory}/${name}\_${alg}\_${start}.$ext
    start=`expr $start + $step`

done
