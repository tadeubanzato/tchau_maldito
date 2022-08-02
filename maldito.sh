#!/bin/sh
## maldito.sh
## Make executable chmod u+x check.sh

CHECK=/tmp/maldito.pid
if [ -f "$CHECK" ]; then
    echo "$CHECK exists."
else
    echo "$CHECK does not exist."
    cd /home/tbanzato/twitter-bots/tchau_maldito
    screen -dm -S maldito python3 tchau_maldito.py
fi
