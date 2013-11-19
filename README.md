mediator
========

### Media library manager

mediator is a torrent-based management package specific to media libraries. It is currently a work in-progress. mediator is intended to be used in conjunction with clients that support script-calling on download completion (e.g. Transmission). The goal is to create a logical taxonomy for personal movie/TV/media libraries, capable of being parsed by frontend media streamers (e.g. Boxee, XBMC), all without sacrificing seeding requirements.

A logical taxonomy depends on proper naming conventions - something that is more or less adhered to by private communities. There are *always* exceptions to this, so the plan is for mediator to by default supply media metadata by opt-in to ensure not 95, not 99, but **100 percent** accuracy in nomenclature. The method for providing suggested metadata is by calling TVDB in conjunction with pattern matching. Because the media source is not controlled, the brute force approach to attaining 100% accuracy would be to include pattern matching for every possible naming structure in every possible private community; don't bother with public communities.

*mediator is being developed with a headless Linux server in mind and is written in mostly Python.*

Status
======

### Metadata scraper

Running regex over each torrent name returns its "best guess" as to which media type it's dealing with; the type it detects is set to the default operation (e.g. [M/e/s/k/i] if a movie, [E/m/s/k/i] if an episode, ...). There are additional checks that can be made to improve accurate detection: file size, file type, extension, etc.

For clarification, the only metadata that mediator should care about is (and should be of the following forms):

* Movies: Title_(Year).extension
* TV Episodes: Name_of_Series.S01E05_-\_Name_of_episode.extension

<sup>*S = Season, E = Episode</sup>

Why? Because front-end media players can parse this format. They are also *very* human-readable. We don't care about the junk embedded in torrent names, like `Breaking.bad_SceneHD.720p.BluRayxHDDVD.x264-DEMAND.mkv`, because *mediator only uses hard links from your bittorrent client's download directory to your media library.* Not only does this method save tremendous storage space, but also keeps your torrents seeding — a primary goal of this project.

Things left to do
=================

### Data serialization/storage

Currently exploring different options to store data. Things considered so far: JSON, Yaml, CSV, shelve, and sqlite. It is desired to store each cleaned media item; `MediaBuilder.build_media()` generates and returns an instance of a `Torrent` class. Due to the nature of what is being stored, it might be advantageous to be human-readable. Euphemisms aside, I've played with `pickle` thus far.

### Daemonize

Run on schedule in background, transmit reports, add non-interactive interface?

### Library enrollment and management

Most people already have a media library they are working with in some capacity. There needs to be an enrollment process for existing libraries.
Library verification and restoration are up for consideration once the primary functions of mediator are in a satisfactory state. This means being able to reconstruct a media library in case of data failure/errors/other unforseen hiccups. Additionally, at some point, a given torrent will no longer need/want to be seeded. There should be a mechanism to stop seeding and replace the hard link with the actual source media.

Currently, `migrate.py` takes a client's torrent library items and merges them into mediator with deduplication. This is currently implemented for Transmission (/var/lib/transmission-daemon/info/torrents), but can be easily modified for any other client's torrent library location.

Functionality
=============

### mediator.py

Control flow script iterates through queue of torrents to-be-processed and stores returned Torrent instance in database.

###  migrate.py

Merges client torrent library with mediator's with duplication checking.

### queue.py

mediator currently manages torrents through three logs: todo, history, and delta. todo is for torrents that have yet to run through mediator. history is self-explanatory. delta is for torrents that have run through mediator, but have either: failed to link, been skipped, or error-ed out.

### torrent.py

Class definition and functions for MediaBuilder. MediaBuilder handles the heavy-lifting for building each torrent: grabs metadata from TVDB and confirms it from stdin, selects the proper source files which will be hard linked, formats the hard link's filename using the collected metadata, and finally links the media to the proper destination. build_media() returns a Torrent class instance which should be handled by the calling instance of MediaBuilder.