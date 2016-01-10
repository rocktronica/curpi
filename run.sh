#!/bin/bash

screen -S curpi_app -dm bash -c 'while true; do
    sudo python app.py
    sleep 5
done'
