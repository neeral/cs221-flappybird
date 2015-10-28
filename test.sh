#!/bin/bash

echo "running $0"
rm *.pyc
rm test.txt
for i in `seq 1 20`;
do
    echo $i
    `{ time python flappybird.py; } >> test.txt 2>> test.txt`
done

exit 1
