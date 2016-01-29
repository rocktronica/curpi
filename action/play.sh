#!/bin/bash
{

dir=$(dirname $0)

# Kill any preexisting players or related processes
sh $dir/stop.sh

# Create a named pipe to hold stream
mkfifo /tmp/stream

# In a screen to contain the process, dump external stream into pipe
screen -S curpi_play_1 -dm bash -c 'rtmpdump -r "rtmp://wowza.stream.publicradio.org/current-iheart/current-iheart.stream" --live -o /tmp/stream'

# Again in a screen, play the piped stream
screen -S curpi_play_2 -dm bash -c 'mplayer /tmp/stream'

}
