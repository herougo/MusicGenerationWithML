from mido import MidiFile, MidiTrack, Message, MetaMessage
import os
from other_util import *
from music_theory import Harmony

def intRoundUp(n, mod):
	return (n + mod - 1) % mod

class NoteSequence():
	def __init__(self, ppqn):
		self.ppqn = ppqn
		self.notes = []
		self.length = 0
		# MIDI leaves a small rest before the next note so we "round" the endings
		# to where they are supposed to be by using epsilon (sixteenth note)
		self.epsilon = ppqn / 4

	def addNote(self, note_midi, start_time, end_time):
		notes.append([note_midi, start_time, end_time])
		self.length = max(end_time, self.length)

	def _cleanNotesAndLength(self):
		self.notes = sorted(self.notes)
		self.length = intRoundUp(self.length, self.ppqn)

	def toMelody(self):
		if len(self.notes) == 0:
			return []

		self._cleanNotesAndLength()

		melody = []
		melody_time_intervals = []

		prev_note = self.notes[0]
		for note in self.notes[1:]:
			pause_btn_notes = note[1] - prev_note[2]
			cgGe(pause_btn_notes, 0, "melody overlap")

			if pause_btn_notes <= self.epsilon:
				prev_note[2] = note[1]
			else:
				rounded_up = intRoundUp(prev_note[2], self.epsilon)
				if rounded_up <= note[1]:
					prev_note[2] = rounded_up
				else:
					raise Exception("No MIDI end adjusting")

			melody.append(prev_note[0])
			melody_time_intervals.append(prev_note[1:3])

		prev_note[2] = intRoundUp(prev_note[2], self.epsilon)
		melody.append(prev_note[0])
		melody_time_intervals.append(prev_note[1:3])

		return melody, melody_time_intervals

	def toHarmony(self):
		if len(self.notes) == 0:
			return []

		self._cleanNotesAndLength()

		prev_end = 0
		time_intervals = []
		note_lists = []
		counter = 0


		for note in self.notes:
			note_start = note[1]
			
			if note_start > prev_end:
				prev_end = note[2]
				counter += 1
				time_intervals.append(note[1:3])
				note_lists.append([note[0]])
			else:
				chEq(time_intervals[counter][0], note[1], "harmony time start matchup")
				chEq(time_intervals[counter][1], note[2], "harmony time end matchup")

				note_lists[counter].append(note[0])

		time_intervals[counter][1] = time_intervals[counter][1], intRoundUp(self.ppqn)

		# make start times on the beat
		for i in range(len(note_lists)):
			time_intervals[counter][0] = intRoundUp(time_intervals[counter][0], ppqn)

		# make the end times of chord the start time of the next chord
		for i in range(len(note_lists) - 1):
			time_intervals[i][1] = ime_intervals[i+1][0]

		chords = map(lambda x: Harmony(note_list=x), note_lists)


		return chords, time_intervals


class Song():
	def __init__(self):
		self.melody = []
		self.melody_time_intervals = []
		self.chords = []
		self.chord_time_intervals = []
		self.bpm = 120
		self.time_sig = [4, 4]
		self.key_sig = 'C'
		self.instrument = 1 # always piano
		self.ppqn = 480

	def loadMidi(self, file_name):
		mid = MidiFile(file_name)
		self.ppqn = mid.ticks_per_beat # ie pulses per quarter note

		chGe(len(mid.tracks), 2, "n_tracks")

		melody_seq = self.parseTrack(mid.tracks[0])
		self.melody, self.melody_time_intervals = melody_seq.toMelody()

		harmony_seq = self.parseTrack(mid.tracks[1])
		self.chords, self.chord_time_intervals = harmony_seq.toHarmony()
		
		return notes

	def parseTrack(self, track):
		seq = NoteSequence(self.ppqn)
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

				seq.addNote(msg.note, note_starts[msg.note], acc_time)

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
				self.bpm = int((60 * 1000 * 1000) / tempo)
		
		chEq(len(note_starts.keys()), 0, "note_dictionary_empty")

		return seq

	def toMidi(self, file_name):
		mid = MidiFile()
		mid.ticks_per_beat = self.ppqn

		raise NotImplementedException()

		# Melody
		melody_track = MidiTrack()
		midi_tempo = int(round((60 * 1000000) / self.bpm))
		melody_track.append(MetaMessage('set_tempo', tempo=midi_tempo))
		melody_track.append(MetaMessage('time_signature', numerator=self.time_sig[0], 
			denominator=self.time_sig[1], clocks_per_click=24, notated_32nd_notes_per_beat=8))
		mid.tracks.append(melody_track)

		melody_track.append(Message('program_change', channel=1, program=1, time=0))

		current_time = 0
		for note, time in zip(self.melody, self.melody_time_intervals):
			wait_delta = time[0] - current_time
			note_length = time[1] - time[0]

			melody_track.append(Message('note_on', note=note, velocity=64, time=wait_delta))
			melody_track.append(Message('note_off', note=note, velocity=64, time=note_length))
			current_time = time[1]

		melody_track.append(MetaMessage('end_of_track'))


		# Harmony
		harmony_track = MidiTrack()
		harmony_track.append(MetaMessage('set_tempo', tempo=midi_tempo))
		harmony_track.append(MetaMessage('time_signature', numerator=self.time_sig[0], 
			denominator=self.time_sig[1], clocks_per_click=24, notated_32nd_notes_per_beat=8))
		mid.tracks.append(harmony_track)

		harmony_track.append(Message('program_change', channel=2, program=1, time=0))

		current_time = 0
		for chord, time_interval in zip(self.chords, self.chord_time_intervals):
			wait_delta = time[0] - current_time
			note_length = time[1] - time[0]
			note_list = chord.getLhChord()

			harmony_track.append(Message('note_on', note=note_list[0], velocity=64, time=wait_delta))
			for note in note_list[1:]:
				harmony_track.append(Message('note_on', note=note, velocity=64, time=0))

			harmony_track.append(Message('note_off', note=note_list[0], velocity=64, time=note_length))
			for note in note_list[1:]:
				harmony_track.append(Message('note_off', note=note, velocity=64, time=0))

			current_time = time[1]


		harmony_track.append(MetaMessage('end_of_track'))

		mid.save(file_name)

	def __str__(self):
		pass
	

if __name__ == "__main__":
	mypath = "siraj-music"
	siraj_files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	siraj_files = filter(lambda x: x.endswith(".midi"), siraj_files)
	for f in siraj_files:
		base_name = os.path.basename(f)
		output_path = os.path.join("Generated/", base_name)

		song = Song()
		song.loadMidi(f)
		song.toMidi(output_path)
		break

	print arr