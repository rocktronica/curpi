#!/bin/bash

# Kill any preexisting players or related processes
sh stop.sh

# Create a named pipe to hold stream
mkfifo /tmp/stream

# In a screen to contain the process, dump external stream into pipe
screen -dm bash -c 'rtmpdump -r "rtmp://wowza.stream.publicradio.org/current-iheart/current-iheart.stream" --live -o /tmp/stream'

# Again in a screen, play the piped stream
screen -dm bash -c 'omxplayer /tmp/stream'
