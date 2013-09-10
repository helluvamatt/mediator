class Torrent:

    MOVIE = 1
    EPISODE = 2
    SEASON = 3
    _type = -1

    def __init__(self, name, media_type):

        self.name = name
        Torrent._type = media_type

    def set_library_path(self, file):

        if file:
            self.library_path = file
            print("lib path set to: %s" % self.library_path)

    def set_metadata(self, **kwargs):

        self.metadata = kwargs.copy()

    def set_filename(self, name, ext):

        self.filename = name
        self.extension = ext

def is_media_type(torrent):
    
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

def collect_metadata(torrent):

    media_type = torrent._type

    if media_type == Torrent.MOVIE:
        title = raw_input("Title: ")
        year = raw_input("Year: ")
        return {
                'title': title,
                'year': year
               }

    elif media_type == Torrent.EPISODE:
        series = raw_input("Series: ")
        season = raw_input("Season: ")
        episode = raw_input("Episode: ")
        return {
                'series': series,
                'season': season,
                'episode': episode
               }

    elif media_type == Torrent.SEASON:
        series = raw_input("Series: ")
        season = raw_input("Season: ")
        return {
                'series': series,
                'season': season
               }
