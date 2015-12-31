#!/bin/bash
{

dir=$(dirname $0)

pids=$(ps aux | grep -v 'SCREEN' | grep '[/]tmp/stream' | awk '{print $2}')
for pid in $pids; do
    kill -9 $pid
done

# Remove old named pipe
rm -f /tmp/stream

# Wipe dead screens
screen -wipe > /dev/null

}
