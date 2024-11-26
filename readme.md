a mettre dans cron ( via sudo crontab -u louis -e )


@reboot sleep 12 && cd /media/usb-seagate2/dev/git/server_https && export MDP=xxx && GARAGE_URL=http://192.168.1.95:80/xxxxx && make run >> /tmp/traceServer.trc 2>&1



## pour espionner le flux avec ezviz

but : récupérer les videos stockés dans les cartes sd des cameras en utilisant l'api

approche : lancer l'appli windows "EzvizStudio" via wine
utiliser le trick man-in-the-middle : mitmweb
ca crée un proxy derrier lequel wine s'exécute

lancer le proxy mitm qui va analyser le flux de commande
       mitmweb -p 8080


avec la bash fonction :
     function ezviz() {
              wine /mnt/NUC/download/EzvizStudioSetups\(1\).exe
     }


lancer Ezviz studio derrier le proxy
       http_proxy=http://127.0.0.1:8080 ezviz


l'approche lancer wine derriere un proxy



