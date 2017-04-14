from util.other_utils import chEq
from util.music_parsing import Song
import numpy as np

# I vi IV V, I V vi IV, IV I V vi

def generateRandomSong():
    # firugre out chord stuff
    raise NotImplementedException()


SIXTEENTH_BAR_LEN = 4 * 16
RANDOM_SONG_ARR_LEN = 4 * SIXTEENTH_BAR_LEN




''' Unused
	def iterBars(self):
		return SongBarIterator(self)

	def iterChords(self):
		pass
	'''
		
''' Unused
class SongBarIterator:
	def __init__(self, song):
		if song.time_sig != [4, 4]:
			raise NotImplementedException("iterBars time signature {}".format(self.time_sig))
		self.song = song
		self.bar_len = song.ppqn * 4
		self.time_position = 0
		self.melody_index_position = 0
		self.chord_index_position = 0

		self.melody_len = len(song.melody)
		self.chords_len = len(song.chords)
	
	def __iter__(self):
		return self

	def next(self):
		if self.melody_index_position >= self.melody_len:
			raise StopIteration
		else:
			# get melody
			start = self.melody_index_position
			i = 0
			while (start + i < self.melody_len 
				and self.song.melody[start + i]): ******
				i += 1
			self.time_position += self.bar_len

			# get chords
			# ***********
'''

if __name__ == "__main__":
	'''
    restbar = [-2] * SIXTEENTH_BAR_LEN
    fullbar = [1] * SIXTEENTH_BAR_LEN
    test1 = restbar + fullbar + restbar
    test2 = fullbar
    test3 = restbar + fullbar
    test4 = fullbar + restbar

    test5 = fullbar * 2 + restbar + fullbar

    splitSixteenthArray(test5)
    '''