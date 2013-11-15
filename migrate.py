#!/usr/bin/env python
import os
import re

def migrate(client_torrents=None):

    if not client_torrents:
        client_torrents = "/var/lib/transmission-daemon/info/torrents"

    for torrent in os.listdir(client_torrents):
        with open("logs/foobar.log" , 'r+a') as log:
            if not any(re.match('(.*)(?=\..*.torrent)', torrent).group(0) in items for items in log):
                log.write("%s\n" % re.match('(.*)(?=\..*.torrent)', torrent).group(0))

def main():

    migrate()
    
if __name__ == '__main__':
    main()
