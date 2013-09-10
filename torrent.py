import os
from readjson import read_json

settings_file = "settings.json"
settings = read_json(settings_file)

class Torrent:

    MOVIE = 1
    EPISODE = 2
    SEASON = 3
    _type = -1

    def __init__(self, name, media_type, library_path, **metadata, filename, extension):

        self.name = name
        self.media_type = media_type
        self.library_path = library_path
        self.metadata = metadata.copy()
        self.filename = filename
        self.extension = extension

class MediaBuilder:

    def __init__(self, name, media_type):

        self.name = name
        self.media_type = media_type

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
    
        os.chdir(settings["torrent-library"])

        for current_file in os.listdir("%s" % self.name):
            if any(current_file.endswith(x) for x in settings["extensions"]):
                source = raw_input("%s? [y/n]" % current_file)
                if source == 'y' or source == '':
                    self.source_file = current_file

        self.extension = os.path.splitext(self.source_file)[1]

    def preexisting(self):

        if self.media_type == Torrent.MOVIE:
            print("checking for movie...")

            if os.path.exists("%s/%s%s" % (
                settings['movie-dir'],
                self.filename,
                self.extension)
            ) or os.path.exists("%s/%s" % (
                settings['movie-dir'],
                self.filename)
            ):
                print("%s/%s%s exists" % (
                    settings['movie-dir'],
                    self.filename,
                    self.extension)
                )
                return True
            else:
                print("%s/%s%s doesn't exist" % (
                    settings['movie-dir'],
                    self.filename,
                    self.extension)
                ) 
                return False

        elif self.media_type == Torrent.EPISODE:
            print("checking for episode..")



        elif self.media_type == Torrent.SEASON:
            print("checking for season...")

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
        os.link(self.source_file, "%s/%s%s" % (settings['movie-dir'], self.filename, self.extension))

        return Torrent(self.name, self.media_type, self.source_file, **self.metadata, self.filename, self.extension)
