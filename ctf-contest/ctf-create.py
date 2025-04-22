# We will need to pip-install the following library for this to work.
#
# pip install pyyaml
#
# This is just an example of how to parse YAML data.  You will need
# to modify this code to generate the files described in the
# Canvas assignment.

import yaml

FILENAME = 'ctf.yml'

# Parse the YAML
data = yaml.safe_load(open(FILENAME).read())

# Accessing parsed data
teams = data['ctf']['teams']
services = data['ctf']['services']

print(teams)
print(services)
