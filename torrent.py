import os
from readjson import read_json

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

    def __init__(self, name, media_type, settings_file):

        self.name = name
        self.media_type = media_type
        self.settings = read_json(settings_file)

    def collect_metadata(self):

        if self.media_type == Torrent.MOVIE:
            title = raw_input("Title: ")
            year = raw_input("Year: ")
            self.metadata = {
                             'title': title,
                             'year': year
                            }

        elif self.media_type == Torrent.EPISODE:
            series = raw_input("Series: ")
            season = raw_input("Season: ")
            episode = raw_input("Episode: ")
            self.metadata = {
                             'series': series,
                             'season': season,
                             'episode': episode
                            }

        elif self.media_type == Torrent.SEASON:
            series = raw_input("Series: ")
            season = raw_input("Season: ")
            self.metadata = {
                             'series': series,
                             'season': season
                            }

    def verify_source_data(self):
    
        os.chdir(self.settings["torrent-library"])

        for current_file in os.listdir("%s" % self.name):
            if any(current_file.endswith(x) for x in self.settings["extensions"]):
                source = raw_input("%s? [y/n]" % current_file)
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
            self.filename = "%s.S%sE%s_-_" % (
                self.metadata['series'].replace(" ", "_"),
                self.metadata['season'],
                self.metadata['episode']
            )

    def build_media(self):

        os.chdir(self.name)

        if self.media_type == Torrent.MOVIE:
            os.link(self.source_file, "%s/%s%s" % (self.settings['movie-dir'], self.filename, self.extension)) 
               
        elif self.media_type == Torrent.EPISODE:
            os.makedirs("%s/%s/Season %s" % (
                self.settings['tv-dir'],
                self.metadata['series'],
                self.metadata['season']))
            os.link(self.source_file, "%s/%s/Season %s/%s%s" % (
                self.settings['tv-dir'],
                self.metadata['series'],
                self.metadata['season'],
                self.filename,
                self.extension))

        return Torrent(self.name, self.media_type, self.source_file, self.filename, self.extension, **self.metadata)
