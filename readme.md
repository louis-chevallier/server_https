a mettre dans cron ( via sudo crontab -u louis -e )


@reboot sleep 12 && cd /media/usb-seagate2/dev/git/server_https && GARAGE_URL=http://192.168.1.95:80/xxxxx && make run >> /tmp/traceServer.trc 2>&1
