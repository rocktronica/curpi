#!/bin/bash

{

if [ "$1" == '-h' ]; then
    echo \
'Usage: ./deploy_to_pi.sh [FILE(S)] [OPTION]

Options:
  -p Relate path of Python script to sudo run after upload'
    exit 1
fi

if [ -z $1 ]; then
    rsync --exclude=".*/" --delete-excluded -avz ~/curpi/ tommy@curpi.local:~/curpi/
else
    rsync -avz $1 tommy@curpi.local:~/curpi/
fi

if [ "$2" == '-p' ]; then
    if [ -z $3 ]; then
        echo 'Missing path argument'
        exit 1
    fi

    ssh tommy@curpi.local "sudo python ~/curpi/$1"
fi

}
