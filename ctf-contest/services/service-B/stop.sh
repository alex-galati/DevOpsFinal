#!/bin/bash

if [[ -f flask.pid ]]; then
    kill "$(cat flask.pid)" && echo "Stopped."
    rm flask.pid
else
    echo "No stored PID found."
fi
