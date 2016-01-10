#!/bin/bash

screen -S curpi_app -dm bash -c 'while true; do
    sudo python app.py
    sleep 5
done'

screen -S curpi_hardware -dm bash -c 'while true; do
    sudo python hardware.py
    sleep 5
done'
