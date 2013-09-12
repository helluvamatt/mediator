#!/usr/bin/env python

import os
import logging
from queue import TorrentQueues
from torrent import Torrent, MediaBuilder

settings_file = "settings.json"

def is_media_type():
        
    media_type = raw_input("movie, episode, season, skip, or ignore? [m/e/s/k/i]")
    
    if media_type == 'm':
        return Torrent.MOVIE

    elif media_type == 'e':
        return Torrent.EPISODE

    elif media_type == 's':
        return Torrent.SEASON

    elif media_type == 'k':
        return

    elif media_type == 'i':
        return

    else:
        print("Invalid input. Try again.")
        is_media_type(torrent)

def main():

    # first, update the queues and store values
    tq = TorrentQueues(settings_file)

    # now, iterate on each torrent in queue
    for i, torrent in enumerate(tq.get_queue(todo=True)):
        torrent = torrent.strip()
        print("[%s/%s] %s:" % (i, tq.todo_size, torrent))
        
        media_type = is_media_type()

        if media_type:
            mb = MediaBuilder(torrent, media_type, settings_file)

            mb.collect_metadata()
            mb.verify_source_data()
            mb.format_filename()

            if not mb.preexisting():
                mb.build_media()

if __name__ == '__main__':
    main()