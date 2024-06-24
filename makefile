

DEPLOY_DIR = /deploy
export DATE:=$(shell date +%Y-%m-%d_%Hh%Mm%Ss)
export HOST=$(shell hostname)
SHELL=bash
export GITINFO=$(shell git log --pretty=format:"%h - %an, %ar : %s" -1)


start1 : server_nuc

start : run1

bbox :
	python bbox.py

server_nuc : pem 
#	ip -f inet addr show eth1 | awk '/inet / {print https://$2:8080}'
	date
	python -c 'import server; server.go()'

run :
	date
	source ${HOME}/scripts/.bashrc; spy; pyenv; make server_nuc




deploy :
	cd $(DEPLOY_DIR); rm -fr server_https; git clone  https://github.com/louis-chevallier/server_https.git; cd server_https; make dopem

run1 :
	date
	source ${HOME}/scripts/.bashrc; spy; pyenv; export MDP=xxx ; make server_nuc

dopem :
	-rm *.pem
	make pem

pem : privkey.pem  privkey.pem

%.pem :
# https://docs.cherrypy.dev/en/latest/deploy.html
	openssl genrsa -out privkey.pem 2048
	openssl req -new -x509 -days 365 -key privkey.pem -out cert.pem
