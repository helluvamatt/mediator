#!/usr/bin/env python

import os
import logging
from readjson import read_json
from queue import TorrentQueues
from format import FormatMedia
from torrent import Torrent, is_media_type, collect_metadata
from sh import sh

settings = "settings.json"
json_file = read_json(settings)

def verify_source_data(torrent):
    
    os.chdir(json_file["torrent-library"])
    for file in os.listdir("%s" % torrent.name):
        if any(file.endswith(x) for x in json_file["extensions"]):
            source = raw_input("%s? [y/n]" % file)
            if source == 'y' or source == '':
                return file

def get_extension(torrent):

    return os.path.splitext(torrent.library_path)[1]

def preexisting(torrent):

    if torrent._type == Torrent.MOVIE:
        print("checking for movie...")

        if os.path.exists("%s/%s%s" % (
            json_file['movie-dir'],
            torrent.filename,
            torrent.extension)
        ) or os.path.exists("%s/%s" % (
            json_file['movie-dir'],
            torrent.filename)
        ):
            print("%s/%s%s exists" % (
                json_file['movie-dir'],
                torrent.filename,
                torrent.extension)
            )
            return True
        else:
            print("%s/%s%s doesn't exist" % (
                json_file['movie-dir'],
                torrent.filename,
                torrent.extension)
            ) 
            return False

    elif torrent._type == Torrent.EPISODE:
        print("checking for episode..")



    elif torrent._type == Torrent.SEASON:
        print("checking for season...")

def insert_to_media(torrent):
    # os.makedirs("%s/%s" % (json_file['movie-dir'], torrent.filename))
    # os.chdir(json_file["torrent-library"])
    os.chdir(torrent.name)
    os.link(torrent.library_path, "%s/%s%s" % (json_file['movie-dir'], torrent.filename, torrent.extension))

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
            f = FormatMedia()

            t.set_metadata(**collect_metadata(t))
            t.set_library_path(verify_source_data(t))
            t.set_filename(f.format(t), get_extension(t))

            if not preexisting(t):
                insert_to_media(t)


if __name__ == '__main__':
    main()