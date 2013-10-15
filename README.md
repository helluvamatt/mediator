mediator
========

### Media library manager

mediator is a torrent-based management package specific to media libraries. It is currently a work in-progress. mediator is intended to be used in conjunction with Transmission or other clients that support script-calling on download completion. The goal is to create a logical taxonomy for personal movie/TV/media libraries, capable of being parsed by frontend media streamers (such as Boxee or XBMC), all without sacrificing seeding requirements.

~~Current plans are to keep management a manual, hands-on approach to ensure that media nomenclature is 100% accurate. Naming and linking automation might be possible, but will only be included at later stages via suggested data.~~ Initial assumptions have been improved upon. It's nowhere near perfect, but using TVDB in conjunction with pattern matching, this is possible.

*mediator is being developed with a headless Linux server in mind and is written in mostly Python.*

Things left to do
=================

### Data serialization/storage

Currently exploring different options to store data. Things considered so far: JSON, Yaml, CSV, shelve, and sqlite. It is desired to store each cleaned media item; `MediaBuilder.build_media()` generates and returns an instance of a `Torrent` class. Due to the nature of what is being stored, it might be advantageous to be human-readable. Euphemisms aside, I've played with `pickle` thus far.

### Metadata scraper

For as many media managers that are out there, there seem to be just as many different metadata parsers — most look to be using `tvdb_api` as a backend. I'm not currently, nor likely ever will be, sold 100% on the accuracy of automatic metadata parsing. The source of our media is torrent trackers maintained by error-prone humans. Every private community seems to use a somewhat different convention for file naming, and even then, their adherance to the rules isn't always consistent; don't even bother with the public trackers.

~~So for now, mediator will retrieve what it *thinks* to be correct and will present the **suggestion** to the user to either accept them suggestion or to enter their own, correct metadata.~~ Right now, mediator is inspecting each torrent name and checking it against 3 regex patterns (one of movies, one for episodes, one for season packs). The accuracy isn't 100% and won't *ever* be – there are just too many edge cases that can't be accounted for. Running regex over each torrent name returns its "best guess" as to which media type it's dealing with; the type it detects is set to the default operation ([M/e/s/k/i] if a movie, [E/m/s/k/i] if an episode, ...). There are additional checks that can be made to improve accurate detection: file size, file type, extension, etc.

For clarification, the only metadata that mediator should care about is (and should be of the following forms):

* Movies: Title_(Year).extension
* TV Episodes: Name_of_Series.S01E05_-_Name_of_episode*.extension

<sup>*S = Season, E = Episode</sup>

Why? Because the best front-end media players can parse these with impeccable accuracy. They are also *very* human-readable. We don't care about the junk embedded in torrent names, like `Breaking.bad_SceneHD.720p.BluRayxHDDVD.x264-DEMAND.mkv`, because *mediator only uses hard links from your bittorrent client's download directory to your media library!* Not only does this method save tremendous storage space, but also keeps your torrents seeding — a primary goal of this project.

### Daemonize

Run on schedule in background, transmit reports, add non-interactive interface?

### Series season handling

~~A season pack of a TV series needs to be handled. One method is to treat a season as a collection of episodes, iterating through each one with some assumptions in metadata application.~~ Season packs are now handled by iteration on a directory. It's dirty; maybe a future enhancement would be to make a SeasonPack subclass of MediaBuilder?

### Library restoration and migration

Most people already have a media library they are working with in some capacity. There needs to be an enrollment process for existing libraries.
Library verification and restoration are up for consideration once the primary functions of mediator are in a satisfactory state. This means being able to reconstruct a media library in case of data failure/errors/other unforseen hiccups. Additionally, at some point, a given torrent will no longer need/want to be seeded. There should be a mechanism to stop seeding and replace the hard link with the actual source media.
