from util.other_utils import chEq
from util.music_parsing import Song
import numpy as np

# I vi IV V, I V vi IV, IV I V vi

def generateRandomSong():
    # firugre out chord stuff
    raise NotImplementedException()


SIXTEENTH_BAR_LEN = 4 * 16
RANDOM_SONG_ARR_LEN = 4 * SIXTEENTH_BAR_LEN

def splitMidi(input_file_path, output_file_prefix):
    full = Song()
    full.loadFromMidi(input_file_path)

    raise NotImplementedException()

    sixteenth_arr = full.toSixteenthArray()

    for i, section_arr in enumerate(splitSixteenthArray(sixteenth_arr)):
        section = Song()
        section.loadFromSixteenthArray(section_arr)
        section.toMidi(output_file_prefix + str(i) + ".mid")


# input: take array of size n * 4 *16, where n is the # of bars
# output: array of arrays corresponding to splitting the input array by full
# bars of rest
def splitSixteenthArray(sixteenth_arr):
    sixteenth_arr = np.array(sixteenth_arr)
    sixteenth_arr_len = len(sixteenth_arr)
    chEq(sixteenth_arr_len % SIXTEENTH_BAR_LEN, 0, "splitSixteenthArray input len")
    start = 0
    end = SIXTEENTH_BAR_LEN

    result = []

    while True:
        # ignore rest
        while np.all(sixteenth_arr[start:end] == -2):
            start += SIXTEENTH_BAR_LEN
            end += SIXTEENTH_BAR_LEN
            if end > sixteenth_arr_len:
                return result
            
        # find maximal streak of consecutive non-empty bars
        while not np.all(sixteenth_arr[end - SIXTEENTH_BAR_LEN:end] == -2):
            if end == sixteenth_arr_len:
                result.append(sixteenth_arr[start:end])
                return result
            end += SIXTEENTH_BAR_LEN
        end -= SIXTEENTH_BAR_LEN
        
        result.append(sixteenth_arr[start:end])
        
        start = end
        end = start + SIXTEENTH_BAR_LEN


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
    restbar = [-2] * SIXTEENTH_BAR_LEN
    fullbar = [1] * SIXTEENTH_BAR_LEN
    test1 = restbar + fullbar + restbar
    test2 = fullbar
    test3 = restbar + fullbar
    test4 = fullbar + restbar

    test5 = fullbar * 2 + restbar + fullbar

    splitSixteenthArray(test5)