

DEPLOY_DIR = /deploy
export DATE:=$(shell date +%Y-%m-%d_%Hh%Mm%Ss)
export HOST=$(shell hostname)
SHELL=bash
export GITINFO=$(shell git log --pretty=format:"%h - %an, %ar : %s" -1)
WOD="$(shell fortune -s)"

start1 : server_nuc

start : run2

bbox :
	python bbox.py

server_nuc : pem 
#	ip -f inet addr show eth1 | awk '/inet / {print https://$2:8080}'
	date
	python -c 'import server; server.go()'

server_ws :  
#	ip -f inet addr show eth1 | awk '/inet / {print https://$2:8080}'
	date
	python server_websocket.py

run :
	date
	source ${HOME}/scripts/.bashrc; spy; pyenv; make server_nuc

deploy :
	-git commit -a -m $(WOD)
	-git push
	-cd $(DEPLOY_DIR); rm -fr server_https; git clone  https://github.com/louis-chevallier/server_https.git; cd server_https; make dopem

run1 :
	date
	source ${HOME}/scripts/.bashrc; spy; pyenv; export MDP=xxx ; make server_nuc

run2 :
	echo 111
	date
	source ${HOME}/scripts/.bashrc; spy; echo 222; pyenv; export MDP=xxx ; echo 333; make server_ws

dopem :
	-rm *.pem
	make pem

pem : privkey.pem  privkey.pem

%.pem :
# https://docs.cherrypy.dev/en/latest/deploy.html
	openssl genrsa -out privkey.pem 2048
	openssl req -new -x509 -days 365 -key privkey.pem -out cert.pem

ccc :
	echo aaa
