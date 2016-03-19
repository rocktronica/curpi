#!/bin/bash

# TODO: run on boot via /etc/rc.local, fix user mismatch errors (?), and
# pass extra arguments
# sudo -H -u tommy bash -c 'sh /home/tommy/curpi/run.sh &'

{

dir=$(dirname $0)
arguments="$*"

if [ "`hostname`" != 'curpi' ]; then
    echo "Run this on curpi machine, not locally"
    exit 1
fi

screen -S app -X quit
screen -S hardware -X quit

screen -S app -dm bash -c "while true; do
    sudo python $dir/app.py $arguments
    sleep 5
done"

screen -S hardware -dm bash -c "while true; do
    sudo python $dir/hardware.py --debug
    sleep 5
done"

}
