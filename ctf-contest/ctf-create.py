import yaml

FILENAME = 'ctf.yml'

# Parse the YAML
data = yaml.safe_load(open(FILENAME).read())

# Accessing parsed data
teams = data['ctf']['teams']
services = data['ctf']['services']

#--------WRITING THE Dockerfile.ctf-admin--------#
admin = open("Dockerfile.ctf-admin", "w")
admin.write('''
from ubuntu:latest

run apt-get update && apt-get install -y openssh-client sshpass ansible sudo vim make python3-venv fortune cowsay curl

run useradd -m ctf-admin && \
	echo "ctf-admin:123" | chpasswd && \
	echo "ctf-admin ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/ctf-admin && \
	chmod 0440 /etc/sudoers.d/ctf-admin

copy test.sh /home/ctf-admin
run chown -R ctf-admin:ctf-admin /home/ctf-admin/test.sh

user ctf-admin
workdir /
''')

admin.close()
#--------WRITING THE Dockerfile.ctf--------#
ctf = open("Dockerfile.ctf", "w")
ctf.write('''
from ubuntu:latest

run apt-get update && apt-get install -y openssh-server sudo vim python3-venv fortune cowsay

run useradd -m ctf && \
	echo "ctf:123" | chpasswd

RUN mkdir -p /run/sshd

copy services /home/ctf/services
copy ansible-playbooks /home/ctf/ansible-playbooks

RUN chown -R ctf:ctf /home/ctf/ansible-playbooks
run chown -R ctf:ctf /home/ctf/services

expose 22
''')
ctf = open("Dockerfile.ctf", "a")
portNum = 5000
for service in services:
	string = "expose " + str(portNum) + "\n"
	ctf.write(string)
	portNum += 1

ctf.write('''
WORKDIR /home/ctf
CMD ["/usr/sbin/sshd", "-D"]
''')
ctf.close()
#--------WRITING THE docker-compose.yml--------#
compose = open("docker-compose.yml", "w")
compose.write('''
# docker-compose.yml
version: "3"

services:
  ctf-admin:
    build:
      context: .
      dockerfile: Dockerfile.ctf-admin
    container_name: ctf-admin
    volumes:
      - ./ansible-playbooks:/ansible-playbooks
    networks:
      - ctf-network
    command: ["tail", "-f", "/dev/null"]
''')
compose = open("docker-compose.yml", "a")
basePortNum = 5000
for team in teams:
	currentIndex = teams.index(team)
	string = f'''
  {team}: 
    build:
      context: .
      dockerfile: Dockerfile.ctf
    container_name: {team}
    networks:
      - ctf-network
    ports:
      - "{str(basePortNum + (currentIndex * 10))}:22"
'''
	compose.write(string)
	additionalPorts = 0
	for service in services:
		newPort = "      - \"" + str(basePortNum + (currentIndex * 10) + (additionalPorts + 1)) + ":" + str(basePortNum + additionalPorts) + "\"\n"
		compose.write(newPort)
		additionalPorts += 1
compose.write('''
networks:
  ctf-network:
''')
compose.close()
#--------WRITING THE inventory.ini---------#
inventory = open("ansible-playbooks/inventory.ini", "w")
inventory.write("[ctf_servers]\n")

inventory = open("ansible-playbooks/inventory.ini", "a")
for team in teams:
	string = f"{team} ansible_host={team}\n"
	inventory.write(string)
string = '''
[ctf_servers:vars]
ansible_port=22
ansible_user=ctf
ansible_ssh_pass=123
ansible_ssh_common_args=-o StrictHostKeyChecking=no
'''
inventory.write(string)
inventory.close()
#--------WRITING THE start.yml--------#
start = open("ansible-playbooks/start.yml", "w")
string = '''
- name: Set up servers
  hosts: ctf_servers
  tasks:
    - name: Debug current working directory
      ansible.builtin.debug:
        msg: "Working from: /home/ctf"
    - name: Run start.sh in services/service-A
      ansible.builtin.shell: |
        cd services/service-A && bash -x start.sh
      args:
        chdir: /home/ctf
    - name: Run start.sh in services/service-B
      ansible.builtin.shell: |
        cd services/service-B && bash -x start.sh
      args:
        chdir: /home/ctf
'''
start.write(string)
start.close()
#--------WRITING THE stop.yml------#
stop = open("ansible-playbooks/stop.yml", "w")
string = '''
- name: Set up servers
  hosts: ctf_servers
  tasks:
    - name: Run stop.sh in services/service-A
      ansible.builtin.shell: |
        cd services/service-A && ./stop.sh
      args:
        chdir: /home/ctf
    - name: Run stop.sh in services/service-B
      ansible.builtin.shell: |
        cd services/service-B && ./stop.sh
      args:
        chdir: /home/ctf
'''
stop.write(string)
stop.close()
