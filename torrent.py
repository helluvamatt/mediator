import os
from readjson import read_json
import re
import tvdb_api
import inspect

settings_file = "settings.json"

class Torrent:

    MOVIE = 1
    EPISODE = 2
    SEASON = 3
    PACK = 4
    _type = -1

    def __init__(self, name, media_type, library_path, filename, extension, **metadata):

        self.name = name
        self.media_type = media_type
        self.library_path = library_path
        self.filename = filename
        self.extension = extension
        self.metadata = metadata.copy()

class MediaBuilder:

    def __init__(self, name, settings_file, parent=None):

        self.name = name
        self.media_type = ""
        self.settings = read_json(settings_file)
        self.parent = parent

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
            self.media_type = Torrent.MOVIE

        elif self.media_type == Torrent.PACK:
            pass
            
        elif media_type == Torrent.PACK:
            for dirname, dirnames, filenames in os.walk("%s/%s" % (self.settings["torrent-library"], self.name)):
                for subdirname in dirnames:
                    sub_movie = MediaBuilder(subdirname, settings_file, self.name)
                    sub_tor = sub_movie.build_media(media_type=Torrent.MOVIE)

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
            series = raw_input("Series [%s]: " % self.metadata['series'])
            season = raw_input("Season [%s]: " % self.metadata['season'])

            if not series == '':
                self.metadata['series'] = series
            if not season == '':
                self.metadata['season'] = season

        elif media_type == Torrent.SEASON:
            series = raw_input("Series: ")
            season = raw_input("Season: ")

            self.metadata = {
                             'series': series,
                             'season': season
                            }

            t = tvdb_api.Tvdb()
            e = t[self.metadata['series']][self.metadata['season']][self.metadata['episode']]

            episodename = raw_input("Episode Name [%s]: " % e['episodename'])

            if episodename == '':
                self.metadata['episodename'] = e['episodename']
            else:
                self.metadata['episodename'] = episodename

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
                                     'series': match.group('seriesname').replace(".", " "),
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

        self.source_files = []
        self.source_file = None

        if self.parent != None:
            self.name = "/".join((self.parent, self.name))

        if self.media_type == Torrent.MOVIE or self.media_type == Torrent.EPISODE:
            if self.name.endswith(tuple(self.settings["extensions"])) and os.path.exists("%s/%s" %
                (self.settings["torrent-library"], self.name)):
                self.source_file = self.name
                self.extension = os.path.splitext(self.source_file)[1]
            else:
                for dirname, dirnames, filenames in os.walk("%s/%s" % (self.settings["torrent-library"], self.name)):
                    for current_file in sorted(filenames):
                        if any(current_file.endswith(x) for x in self.settings["extensions"]):
                            source = raw_input("%s? [Y/n]" % current_file)
                            if source == 'y' or source == '':
                                self.source_file = current_file
                                break

                    self.extension = os.path.splitext(self.source_file)[1]
        
        elif self.media_type == Torrent.SEASON:
            self.extension = []
            self.pathto = []
            for dirname, dirnames, filenames in sorted(os.walk("%s/%s" % (self.settings["torrent-library"], self.name))):
                for current_file in filenames:
                    if any(current_file.endswith(x) for x in self.settings["extensions"]):
                        if not any(re.search(foo, current_file, re.IGNORECASE) for foo in self.settings["ignore_patterns"]):
                            source = raw_input("%s? [Y/n]" % current_file)
                            if source == 'y' or source == '':
                                self.pathto.append(dirname)
                                self.source_files.append(current_file)
                                self.extension.append(os.path.splitext(current_file)[1])

        if self.source_file != None or self.source_files != []:
            return True
        else:
            return False

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
                overwrite = raw_input("Movie already exists. Overwrite? [Y/n]")
                if overwrite == 'y' or overwrite == '':
                    return False
                else:
                    return True
            else:
                return False

        elif self.media_type == Torrent.EPISODE:
            if os.path.exists("%s/%s/Season %s/%s%s" % (
                self.settings['tv-dir'],
                self.metadata['series'],
                self.metadata['season'],
                self.filename,
                self.extension)
            ):
                overwrite = raw_input("Episode already exists. Overwrite? [Y/n]")
                if overwrite == 'y' or overwrite == '':
                    return False
                else:
                    return True
            else:
                return False

        elif self.media_type == Torrent.SEASON:
            if os.path.exists("%s/%s/Season %s" % (
                self.settings['tv-dir'],
                self.metadata['series'],
                self.metadata['season'])
            ):
                overwrite = raw_input("Season already exists. Overwrite? [Y/n]")
                if overwrite == 'y' or overwrite == '':
                    return False
                else:
                    return True
            else:
                return False

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
                    self.metadata['episodename'].replace(" ", "_")
                )
            else:
                self.filename = "%s.S%02dE%02d" % (
                    self.metadata['series'].replace(" ", "_"),
                    self.metadata['season'],
                    self.metadata['episode']
                )

        if self.media_type == Torrent.SEASON:
            self.filename = []
            for (i, f) in enumerate(self.source_files):

                t = tvdb_api.Tvdb()
                e = t[self.metadata['series']][self.metadata['season']][i+1]

                self.filename.append("%s.S%02dE%02d_-_%s" % (
                    self.metadata['series'].replace(" ", "_"),
                    self.metadata['season'],
                    i + 1,
                    e['episodename'].replace(" ", "_")
                ))

    def build_media(self, media_type=None):

        if self.parent != None:
            print("Sub-pack: %s" % self.name)

        self.collect_metadata(media_type)

        if not self.verify_source_data():
            print("Source data not found. Check library.")
            return False

        self.format_filename()

        if not self.preexisting():

            if self.media_type == Torrent.MOVIE:
                try:
                    os.makedirs("%s/%s" % (self.settings['movie-dir'], self.filename))
                except Exception as e:
                    if e.errno != 17:
                        print("Unexpected: %s\n" % e)

                if self.name != self.source_file:
                    try:
                        os.link("%s/%s/%s" % (self.settings['torrent-library'], self.name, self.source_file),
                                "%s/%s/%s%s" % (self.settings['movie-dir'], self.filename, self.filename, self.extension)) 
                    except Exception as e:
                        if e.errno != 17:
                            print("Unexpected: %s\n" % e)

                else:
                    try:
                       os.link("%s/%s" % (self.settings['torrent-library'], self.source_file),
                                "%s/%s/%s%s" % (self.settings['movie-dir'], self.filename, self.filename, self.extension)) 
                    except Exception as e:
                        if e.errno != 17:
                            print("Unexpected: %s\n" % e)

            elif self.media_type == Torrent.EPISODE:
                try:
                    os.makedirs("%s/%s/Season %s" % (
                        self.settings['tv-dir'],
                        self.metadata['series'],
                        self.metadata['season']))
                except OSError as e:
                    if e.errno != 17:
                        print("Unexpected: %s\n" % e)

                if self.name != self.source_file:
                    try:
                        os.link("%s/%s/%s" % (self.settings['torrent-library'], self.name, self.source_file),
                                "%s/%s/Season %s/%s%s" % (
                                self.settings['tv-dir'],
                                self.metadata['series'],
                                self.metadata['season'],
                                self.filename,
                                self.extension))
                    except Exception as e:
                        if e.errno != 17:
                            print("Unexpected: %s\n" % e)

                else:
                    try:
                        os.link("%s/%s" % (self.settings['torrent-library'], self.source_file),
                                "%s/%s/Season %s/%s%s" % (
                                self.settings['tv-dir'],
                                self.metadata['series'],
                                self.metadata['season'],
                                self.filename,
                                self.extension))
                    except Exception as e:
                        if e.errno != 17:
                            print("Unexpected: %s\n" % e) 

            elif self.media_type == Torrent.SEASON:
                try:
                    os.makedirs("%s/%s/Season %s" % (
                        self.settings['tv-dir'],
                        self.metadata['series'],
                        self.metadata['season']))
                except OSError as e:
                    if e.errno != 17:
                        print("Unexpected: %s\n" % e)

                for (i, f) in enumerate(self.source_files):
                    try:
                        os.link("%s/%s" % (self.pathto[i], f),
                            "%s/%s/Season %s/%s%s" % (
                            self.settings['tv-dir'],
                            self.metadata['series'],
                            self.metadata['season'],
                            self.filename[i],
                            self.extension[i]))
                    except Exception as e:
                        if e.errno != 17:
                            print("Unexpected: %s\n" % e)

                self.source_file = "null"

            return Torrent(self.name, self.media_type, self.source_file, self.filename, self.extension, **self.metadata)
        else:
            return False

