#!/bin/bash
{

dir=$(dirname $0)

# Kill all pipes, streams, screens, and dumps. This is likely not ideal.
kill -9 $(ps aux | grep '[/]tmp/stream' | awk '{print $2}') > /dev/null

# Remove old named pipe
rm -f /tmp/stream

# Wipe dead screens
screen -wipe > /dev/null

}
