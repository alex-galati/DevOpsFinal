#!/bin/bash

python3 -m venv env
if [[ -d env/bin ]]; then
		. env/bin/activate && pip install Flask
	elif [[ -d env/Scripts ]]; then
		. env/Scripts/activate && pip install Flask
	else 
		echo "Failed to create a virtual environment."
	fi

nohup flask run --host=0.0.0.0 --port=5001 &
echo $! >flask.pid 
