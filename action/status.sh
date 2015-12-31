#!/bin/bash
{

dir=$(dirname $0)

# Return the first PID of any relevant process
ps aux | grep '[/]tmp/stream' | head -1 | awk '{print $2}'

# If nothing returns, we know nothing is happening

}
