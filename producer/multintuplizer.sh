#!/bin/bash

#for i in 10 34
for i in {63..124}
#for i in {225..253}
do
    #cmd="python3 picoNtuplizer.py 2p5 /eos/user/j/jleonhol/muonNanoAOD2022F/outntuple_2p5_$i input_files/input_files_$i.txt"
    #cmd="python3 picoNtuplizer.py 2p5 outntuple_2p5_$i input_files/input_files_$i.txt"
    cmd="python3 picoNtuplizer.py -o /eos/user/j/jleonhol/picoNtuples/DY_new/outntuple_2p5_$i -i input_files/input_files_$i.txt -v 2p5 -mc"
    echo $cmd
    ${cmd}
    
done

