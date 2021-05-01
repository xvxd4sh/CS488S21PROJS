#! /usr/bin/env bash

declare -a target_server=("1" "2" "4" "8" "16" "32" "64")

#experiment program run list.

sudo ./project_control.py -d results/1 -n 1 -r 90 -t 30
echo "Experiment with 1 server finished"
sudo ./project_control.py -d results/2 -n 2 -r 90 -t 30
echo "Experiment with 2 servers finished"
sudo ./project_control.py -d results/4 -n 4 -r 90 -t 30
echo "Experiment with 4 servers finished"
sudo ./project_control.py -d results/8 -n 8 -r 90 -t 30
echo "Experiment with 8 servers finished"
sudo ./project_control.py -d results/16 -n 16 -r 90 -t 30
echo "Experiment with 16 servers finished"
sudo ./project_control.py -d results/32 -n 32 -r 90 -t 30
echo "Experiment with 32 servers finished"
sudo ./project_control.py -d results/64 -n 64 -r 80 -t 30
echo "Experiment with 64 servers finished"


echo "Parsing data"
cd results
for i in "${target_server[@]}"
do
    cd "$i"
    cd ../
    python data_parsing.py $i/*.csv > $i.csv
done

gnuplot data_parsing.plt
