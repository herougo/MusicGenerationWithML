from mido import MidiFile, MidiTrack, Message
import os

# Check Equal: Assert that 2 arguments are equal. If they are not raise an exception with a error type
def chEq(x, y, error_type):
	if x != y:
		message = "{} error: {} != {}".format(error_type, x, y)
		raise Exception(message)

# Check Greater than or Equal to
def chGe(x, y, error_type):
	if x < y:
		message = "{} error: {} < {}".format(error_type, x, y)
		raise Exception(message)

def chNotIn(val, my_collection, error_type):
	if val in my_collection:
		message = "{} error: {} in {}".format(error_type, val, my_collection)
		raise Exception(message)

def chIn(val, my_collection, error_type):
	if val not in my_collection:
		message = "{} error: {} not in {}".format(error_type, val, my_collection)
		raise Exception(message)



class Key():
	def __init__(self, tonic, type):
		# ....
	def getLhChord():

	def getMiddleTonic():

class Melody():
	def __init__(self, ppqn):
		self.ppqn = ppqn
		self.notes = []
	def addNote(self, note_midi, start_time, end_time):
		notes.append(note_midi, start_time, end_time)


class Song():
	def __init__(self):
		# epsilon
		self.melody = []
		self.harmony = []
		self.tempo = 120
		self.time_sig = [4, 4]
		self.key_sig = 'C'
		self.instrument = 1 # always piano
	def loadMidi(self, file_name):
		mid = MidiFile(file_name)
		ppqn = mid.ticks_per_beat # ie pulses per quarter note
		acc_time = 0

		chGe(len(mid.tracks), 2, "n_tracks")

		# Melody
		melody = Melody(ppqn)
		acc_time = 0
		track = mid.tracks[0]
		note_starts = {}

		for msg in track:
			if msg.type == 'note_off' or (msg.type == 'note_on' and msg.veloctiy==0):
				# (note_off is equivalent to note_on with 0 velocity)
				# (note that midi files can play notes then leave a brief rest before the next note
				#  which isn't explicitly marked as a rest)
				#print msg.velocity, msg.note, msg.time

				acc_time += msg.time
				chNotIn(msg.note, note_starts.keys(), "note")

				mel.addNote(msg.note, note_starts[msg.note], acc_time)

				del note_starts[msg.note]


			elif msg.type == 'note_on':
				#print msg.velocity, msg.note, msg.time
				# default: velocity 64, otherwise 0
				# note: between 0 and 127 inclusively where 60 is middle C (40th note on piano),
				#       A0 is 21, and C8 is 108
				# time: specifies how much you wait before playing this note next
				#       eg. time=0 means you play it immediately as you get the message
				#       the units are ticks

				acc_time += msg.time
				chIn(msg.note, note_starts.keys(), "note")
				note_starts[msg.note] == acc_time


				#elif msg.type == 'program_change':
				#print msg.program # instrument
				# 1: acoustic grand piano
				# 2-6: other piano types
				#print msg.channel
				# channel where the instrument is used (10 is supposed to be for precussion?)

			elif msg.type == 'key_signature':
				#print msg.key_signature
				# can be 'Dbm' for D flat minor
				# default 'C' for C major
				self.key_sig = msg.key_signature

			elif msg.type == 'time_signature':
				#print msg.numerator, msg.denominator, msg.clocks_per_click
				#print msg.notated_32nd_notes_per_beat
				# default 4, 4, 24, 8

				# I'm not sure how to handle other clocks_per_click and notated_32nd_notes_per_beat values
				chEq(msg.clocks_per_click, 24, "clocks_per_tick")
				chEq(msg.notated_32nd_notes_per_beat, 8, "notated_32nd_notes_per_beat")

				self.time_sig = [msg.numerator, msg.denominator]

			elif msg.type == 'set_tempo':
				#print msg.set_tempo
				# possible: 0 ... 16777215
				# default: 500 000
				# this means 500 000 microseconds (0.5 s) per beat (quarter note)
				# thus the default is 120 BMP (beats per minute)
				self.tempo = int((60 * 1000 * 1000) / tempo)

		chEq(len(notes.keys()), 0, "note_dictionary_empty")
		
		return notes

def noteArrayToMidi(note_array, file_name):
	mid = MidiFile()
	


	mid.save(file_name)

if __name__ == "__main__":
	mypath = "siraj-music"
	siraj_files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	siraj_files = filter(lambda x: x.endswith(".midi"), siraj_files)
	for f in siraj_files:
		arr = midiToNoteArray(f)
		base_name = os.path.basename(f)
		output_path = os.path.join("Generated/", base_name)
		noteArrayToMidi(arr, output_path)

	print arr