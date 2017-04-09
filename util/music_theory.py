import numpy as np
from other_util import chEq

MIDI_MIDDLE_C = 60


MIDI_NUM_TO_NOTE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_TO_LH_ROOT = {
	'C': 48, 
	'C#': 49, 
	'D': 50, 
	'D#': 51, 
	'E': 52, 
	'F': 53, 
	'F#': 42, 
	'G': 43, 
	'G#': 44, 
	'A': 45, 
	'A#': 46, 
	'B': 47
}
SUPPORTED_QUALITIES = {
	'+': np.array([0, 4, 7]),
	'-': np.array([0, 3, 7])
	# aug, dim, dom7, dim7
}

def noteToLhRoot(midi_note):
	return NOTE_TO_LH_ROOT[midi_note]

def midiNumToNote(n):
	# 60 is C
	return MIDI_NUM_TO_NOTE[n % 12]


class Harmony():
	def __init__(self, root='C', quality='+', note_list=[]):
		if len(note_list) > 0:
			if not self.loadNoteList(note_list):
				english_note_list = map(midiNumToNote, note_list)
				raise NotImplementedError((note_list, english_note_list))
		else:
			self.root = root
			self.quality = quality
			if quality not in SUPPORTED_QUALITIES.keys():
				raise NotImplementedError()

	# note list uses the MIDI numbers
	def loadNoteList(self, note_list):
		# C, E, G is C major
		# C#, E# and G# is C# major
		n_notes = len(note_list)
		note_list = np.array(sorted(list(set(map(lambda x: x % 12, note_list)))))
		note_list = np.concatenate([note_list, note_list + 12])

		note_list_diff = np.diff(note_list) # 5

		for k in SUPPORTED_QUALITIES.keys():
			quality_diff = np.diff(SUPPORTED_QUALITIES[k])

			if len(quality_diff) != n_notes - 1:
				# if the number of notes don't match for the quality 
				continue

			for i in range(n_notes):
				if np.all(note_list_diff[i:i+n_notes-1] == quality_diff):
					chord = note_list[i:i+n_notes]
					self.root = midiNumToNote(chord[0])
					self.quality = k

					return True

		return False


	def getLhChord(self):
		root_midi_num = NOTE_TO_LH_ROOT[self.root]
		return root_midi_num + SUPPORTED_QUALITIES[self.quality]

	def fitChord(self, midi_note):
		return (midi_note) % 12 in (self.getLhChord() % 12)

		

def _tests():
	c_note_list = [48, 52, 55]
	har = Harmony(note_list=c_note_list)
	har.loadNoteList(c_note_list)
	print har.root, har.quality
	lh_chord = har.getLhChord()
	
	for x, y in zip(lh_chord, c_note_list):
		chEq(x, y, "lh_chord")
		chEq(har.fitChord(y), True, "fitChord")

	c_minor_note_list = [48, 51, 55]
	har.loadNoteList(c_minor_note_list)
	print har.root, har.quality
	lh_chord = har.getLhChord()
	
	for x, y in zip(lh_chord, c_minor_note_list):
		chEq(x, y, "lh_chord")
		chEq(har.fitChord(y), True, "fitChord")

if __name__ == "__main__":
	_tests()

