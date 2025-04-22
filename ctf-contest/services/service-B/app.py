from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
import subprocess
import os 

app = Flask(__name__)
app.secret_key = 'thereleasedateofhollowknight:silksong'

@app.route('/', methods=['GET'])
def fortune():
	command_string = 'fortune | cowsay -f stegosaurus'
	result = subprocess.run(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	result = str(result.stdout) 
	return f"<pre>{ result }<pre>"	
