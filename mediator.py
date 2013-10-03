#!/usr/bin/env python

import os
import logging
from queue import TorrentQueues
from torrent import Torrent, MediaBuilder
import pickle
import string

settings_file = "settings.json"

def dynamic_options(media_type):

    opt_list = []

    if media_type == 1:
        opt_list.append("M")
        opt_list.append("e")
        opt_list.append("s")
        opt_list.append("i")
    elif media_type == 2:
        opt_list.append("E")
        opt_list.append("m")
        opt_list.append("s")
        opt_list.append("i")
    elif media_type == 3:
        opt_list.append("S")
        opt_list.append("m")
        opt_list.append("e")
        opt_list.append("i")
    else:
        opt_list.append("I")
        opt_list.append("m")
        opt_list.append("e")
        opt_list.append("s")

    opt_list.append("k")

    opt_string = "["

    for i, opt in enumerate(opt_list):
        opt_string = opt_string + "%s" % opt
        if i < len(opt_list) - 1:
            opt_string = opt_string + "/"

    opt_string = opt_string + "]"

    return opt_string

def main():

    # first, update the queues and store values
    tq = TorrentQueues(settings_file)
    pickledb = open("history.pkl", "wb")

    # now, iterate on each torrent in queue
    for i, torrent in enumerate(tq.get_queue(todo=True)):
        torrent = torrent.strip()
        mb = MediaBuilder(torrent, settings_file)

        while True:
            operate = raw_input("[%s/%s] %s %s:" % (i + 1,
                                                    tq.todo_size + 1,
                                                    torrent,
                                                    dynamic_options(mb.get_suggested_metadata())
                                                   )).lower()
            if len(operate) <= 1:
                if operate in string.letters and operate in ['m','e','s','k','i','']:
                    if operate == '':
                        tor = mb.build_media()
                    elif operate == 'm':
                        tor = mb.build_media(media_type=Torrent.MOVIE)
                    elif operate == 'e':
                        tor = mb.build_media(media_type=Torrent.EPISODE)
                    elif operate == 's':
                        tor = mb.build_media(media_type=Torrent.SEASON)    
                    break
                print("Invalid option. Enter either a single letter or return.")
            else:
                print("Invalid option. Enter either a single letter or return.")
        
            pickle.dump(tor, pickledb)

if __name__ == '__main__':
    main()
