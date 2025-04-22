import yaml

FILENAME = 'ctf.yml'

# Parse the YAML
data = yaml.safe_load(open(FILENAME).read())

# Accessing parsed data
teams = data['ctf']['teams']
services = data['ctf']['services']

admin = open("Dockerfile.ctf-admin", "w")
admin.write('''
from ubuntu:latest

run apt-get update && apt-get install -y \
openssh-client sshpass ansible sudo vim make python3.10-venv

run useradd -m ctf-admin && echo "ctf-admin ALL=(ALL) "
''')
