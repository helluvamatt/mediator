#!/usr/bin/env python
import os
import re

for torrent in os.listdir("/var/lib/transmission-daemon/info/torrents"):
    with open("logs/foobar.log" , 'r+a') as log:
        if not any(re.match('(.*)(?=\..*.torrent)', torrent).group(0) in items for items in log):
            log.write("%s\n" % re.match('(.*)(?=\..*.torrent)', torrent).group(0))
