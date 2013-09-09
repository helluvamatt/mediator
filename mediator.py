#!/usr/bin/env python

import os
import logging
from readjson import read_json
from queue import TorrentQueues
from torrent import Torrent, is_media_type, collect_metadata
from sh import sh

settings = "settings.json"
json_file = read_json(settings)

def verify_source_data(torrent):
    
    print("name: %s" % torrent.name)
    os.chdir(json_file["torrent-library"])
    for file in os.listdir("%s" % torrent.name):
        print(file)

def main():

    # first, update the queues and store values
    tq = TorrentQueues(settings)

    # now, iterate on each torrent in queue
    for i, torrent in enumerate(tq.get_queue(todo=True)):
        
        torrent = torrent.strip()
        print("[%s/%s] %s:" % (i, tq.todo_size, torrent))
        
        media_type = is_media_type(torrent)

        if media_type:
            t = Torrent(torrent, media_type)

            t.set_info(**collect_metadata(t))

            verify_source_data(t)


if __name__ == '__main__':
    main()