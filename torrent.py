import os
from readjson import read_json
import re
import tvdb_api

class Torrent:

    MOVIE = 1
    EPISODE = 2
    SEASON = 3
    _type = -1

    def __init__(self, name, media_type, library_path, filename, extension, **metadata):

        self.name = name
        self.media_type = media_type
        self.library_path = library_path
        self.filename = filename
        self.extension = extension
        self.metadata = metadata.copy()

class MediaBuilder:

    def __init__(self, name, settings_file):

        self.name = name
        self.media_type = ""
        self.settings = read_json(settings_file)

        self.get_suggested_metadata()

    def collect_metadata(self, media_type=None):

        if self.media_type == Torrent.MOVIE:
            title = raw_input("Title [%s]: " % self.metadata['title'])
            year = raw_input("Year [%s]:" % self.metadata['year'])

            if not title == '':
                self.metadata['title'] = title
            if not year == '':
                self.metadata['year'] = year

        elif media_type == Torrent.MOVIE:
            title = raw_input("Title: ")
            year = raw_input("Year: ")

            self.metadata = {
                             'title': title,
                             'year': year
                            }

        elif self.media_type == Torrent.EPISODE:
            series = raw_input("Series [%s]: " % self.metadata['series'])
            season = raw_input("Season [%s]: " % self.metadata['season'])
            episode = raw_input("Episode [%s]: " % self.metadata['episode'])

            if not series == '':
                self.metadata['series'] = series
            if not season == '':
                self.metadata['season'] = season
            if not episode == '':
                self.metadata['episode'] = episode

            print("time to query tvdb...")
            t = tvdb_api.Tvdb()
            e = t[self.metadata['series']][self.metadata['season']][self.metadata['episode']]
            episodename = raw_input("Episode Name [%s]: " % e['episodename'])

            if episodename == '':
                self.metadata['episodename'] = e['episodename']
            else:
                self.metadata['episodename'] = episodename

        elif media_type == Torrent.EPISODE:
            series = raw_input("Series: ")
            season = raw_input("Season: ")
            episode = raw_input("Episode: ")

            self.metadata = {
                             'series': series,
                             'season': season,
                             'episode': episode
                            }

            t = tvdb_api.Tvdb()
            e = t[self.metadata['series']][self.metadata['season']][self.metadata['episode']]
            episodename = raw_input("Episode Name [%s]: " % e['episodename'])

            if episodename == '':
                self.metadata['episodename'] = e['episodename']
            else:
                self.metadata['episodename'] = episodename

        elif self.media_type == Torrent.SEASON:
            series = raw_input("Series: ")
            season = raw_input("Season: ")
            self.metadata = {
                             'series': series,
                             'season': season
                            }

    def get_suggested_metadata(self):

        self.compiled_regexs = []

        for cpattern in self.settings["filename_patterns"]:
            cregex = re.compile(cpattern, re.VERBOSE)
            self.compiled_regexs.append(cregex)

        for cmatcher in self.compiled_regexs:
            match = cmatcher.match(self.name)

            if match:
                namedgroups = match.groupdict().keys()

                if 'episodenumber' in namedgroups:

                    self.metadata = {
                                     'series': match.group('seriesname').replace(".", " "),
                                     'season': int(match.group('seasonnumber')),
                                     'episode': int(match.group('episodenumber'))
                                    }
                    self.media_type = Torrent.EPISODE

                elif 'seasonnumber' in namedgroups:
                    self.metadata = {
                                     'series': match.group('seriesname'),
                                     'season': int(match.group('seasonnumber'))
                                    }
                    self.media_type = Torrent.SEASON

                elif 'title' in namedgroups:
                    self.metadata = {
                                     'title': match.group('title').replace(".", " "),
                                     'year': int(match.group('year'))
                                    }
                    self.media_type = Torrent.MOVIE

                else:
                    self.media_type = ""
                
                return self.media_type

    def verify_source_data(self):

        for current_file in os.listdir("%s/%s" % (self.settings["torrent-library"], self.name)):
            if any(current_file.endswith(x) for x in self.settings["extensions"]):
                source = raw_input("%s? [Y/n]" % current_file)
                if source == 'y' or source == '':
                    self.source_file = current_file

        self.extension = os.path.splitext(self.source_file)[1]

    def preexisting(self):

        if self.media_type == Torrent.MOVIE:
            if os.path.exists("%s/%s%s" % (
                self.settings['movie-dir'],
                self.filename,
                self.extension)
            ) or os.path.exists("%s/%s" % (
                self.settings['movie-dir'],
                self.filename)
            ):
                print("movie already exists")
                return True
            else:
                print("movie is new") 
                return False

        elif self.media_type == Torrent.EPISODE:
            if os.path.exists("%s/%s/Season %s/%s%s" % (
                self.settings['tv-dir'],
                self.metadata['series'],
                self.metadata['season'],
                self.filename,
                self.extension)
            ):
                print("episode already exists")
                return True
            else:
                print("episode is new")
                return False


        elif self.media_type == Torrent.SEASON:
            print("seasons not supported yet! perhaps you should get on that?")

    def format_filename(self):

        if self.media_type == Torrent.MOVIE:
            self.filename = "%s_(%s)" % (
                self.metadata['title'].replace(" ", "_"),
                self.metadata['year']
            )

        if self.media_type == Torrent.EPISODE:
            if self.metadata['episodename']:
                self.filename = "%s.S%02dE%02d_-_%s" % (
                    self.metadata['series'].replace(" ", "_"),
                    self.metadata['season'],
                    self.metadata['episode'],
                    self.metadata['episodename']
                )
            else:
                self.filename = "%s.S%02dE%02d" % (
                    self.metadata['series'].replace(" ", "_"),
                    self.metadata['season'],
                    self.metadata['episode']
                )

    def build_media(self, media_type=None):

        self.collect_metadata(media_type)
        self.verify_source_data()
        self.format_filename()

        if not self.preexisting():

            if self.media_type == Torrent.MOVIE:
                os.makedirs("%s/%s" % (self.settings['movie-dir'], self.filename))
                os.link("%s/%s/%s" % (self.settings['torrent-library'], self.name, self.source_file),
                        "%s/%s/%s%s" % (self.settings['movie-dir'], self.filename, self.filename, self.extension)) 
                   
            elif self.media_type == Torrent.EPISODE:
                os.makedirs("%s/%s/Season %s" % (
                    self.settings['tv-dir'],
                    self.metadata['series'],
                    self.metadata['season']))
                os.link("%s/%s/%s" % (self.settings['torrent-library'], self.name, self.source_file),
                        "%s/%s/Season %s/%s%s" % (
                        self.settings['tv-dir'],
                        self.metadata['series'],
                        self.metadata['season'],
                        self.filename,
                        self.extension))

            return Torrent(self.name, self.media_type, self.source_file, self.filename, self.extension, **self.metadata)
        else:
            return False
