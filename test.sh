#!/bin/bash

echo "running $0"
# rm *.pyc
# rm test.txt
for i in `seq 1 10`;
do
    echo 'new run ....'
    echo 'new run ....' >> test6.txt
    echo $i
    echo $i >> test6.txt
    `{ python flappybird.py; } >> test6.txt 2>> test6.txt`
    # `{ time python flappybird.py; } >> test.txt 2>> test.txt`
done

exit 1
