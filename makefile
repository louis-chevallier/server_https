


export DATE:=$(shell date +%Y-%m-%d_%Hh%Mm%Ss)
export HOST=$(shell hostname)
SHELL=bash
export GITINFO=$(shell git log --pretty=format:"%h - %an, %ar : %s" -1)

start1 : server_nuc
start : bbox

bbox :
	python bbox.py

server_nuc : pem 
#	ip -f inet addr show eth1 | awk '/inet / {print https://$2:8080}'
	MDP=xxxx python -c 'import server; server.go()'

run :
	date
	source ${HOME}/scripts/.bashrc; spy; pyenv; make server_nuc


pem : privkey.pem  privkey.pem

%.pem :
# https://docs.cherrypy.dev/en/latest/deploy.html
	openssl genrsa -out privkey.pem 2048
	openssl req -new -x509 -days 365 -key privkey.pem -out cert.pem
