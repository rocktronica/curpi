#!/bin/bash

if [ "`hostname`" != 'curpi' ]; then
    echo "Run this on curpi machine, not locally"
    exit 1
fi

screen -S curpi_app -dm bash -c 'while true; do
    sudo python app.py
    sleep 5
done'

screen -S curpi_hardware -dm bash -c 'while true; do
    sudo python hardware.py
    sleep 5
done'
