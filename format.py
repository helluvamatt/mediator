from torrent import Torrent

class FormatMedia:

	def format(self, torrent):

		if torrent._type == Torrent.MOVIE:
			filename = "%s_(%s)" % (
				torrent.metadata['title'].replace(" ", "_"),
				torrent.metadata['year']
			)
			return filename

		if torrent._type == Torrent.EPISODE:
			filename = "%s.S%sE%s_-_" % (
				torrent.metadata['series'].replace(" ", "_"),
				torrent.metadata['season'],
				torrent.metadata['episode']
			)
			return filename