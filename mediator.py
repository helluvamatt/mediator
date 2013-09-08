#!/usr/bin/env python

import os
import sh
from log import TorrentQueues

settings = "settings.json"

def inspect_media_type(torrent):
    media_type = raw_input("movie, episode, season, skip, or ignore? [m/e/s/k/i]")
    print("type is: %s" % media_type)

def main():

    # first, update the queues and store values
    tq = TorrentQueues(settings)

    # now, iterate on queue
    for n, torrent in enumerate(tq.get_queue(todo=True)):
        print("[%s/%s] %s:" % (n, tq.todo_size, torrent.strip('\n')))
        inspect_media_type(torrent.strip('\n'))

if __name__ == '__main__':
    main()