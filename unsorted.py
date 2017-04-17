from util.other_utils import chEq
from util.music_parsing import Song
import numpy as np

# I vi IV V, I V vi IV, IV I V vi


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

Old Iterate by Chord
def iterByChord(self):
        chord_ranges = getSatisfyingRanges(self._isPartOfChord, self.chords_arr)
        melodies = map(lambda r: self.melody_arr[r], chord_ranges)
        chord_len = len(chord_ranges)

        # account for notes starting before the ranges
        for i in range(chord_len):
            r = chord_ranges[i]
            if melodies[r[0]] == SUSTAIN:
                # extend first note left
                for j in reversed(range(0, r[0])):
                    if melodies[j] != SUSTAIN:
                        melodies[r[0]] = melodies[j]
                        break
            if r[1] < chord_len:
                # extend last note right **************
                for j in range(r[1], chord_len):
                    if melodies[j] != SUSTAIN:
                        melodies[r[0]] = melodies[j]
                        break

        chords = map(lambda r: self.chords_arr[r[0]], chord_ranges)
        section_lengths = map(lambda r: r[1] - r[0], chord_ranges)
        return zip(melodies, chords, section_lengths)
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