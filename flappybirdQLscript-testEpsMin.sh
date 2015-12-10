#!/bin/bash

cmd="python flappybirdQLscript-testEpsMin.py 50"
eval "${cmd}" &>flappybirdQLscript-testEpsMin-50.log &disown

cmd="python flappybirdQLscript-testEpsMin.py 60"
eval "${cmd}" &>flappybirdQLscript-testEpsMin-60.log &disown

cmd="python flappybirdQLscript-testEpsMin.py 80"
eval "${cmd}" &>flappybirdQLscript-testEpsMin-80.log &disown

cmd="python flappybirdQLscript-testEpsMin.py 90"
eval "${cmd}" &>flappybirdQLscript-testEpsMin-90.log &disown

