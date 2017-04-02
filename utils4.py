

def midiToNoteArray(file_name):
	mid = MidiFile(file_name)
	ppqn = mid.ticks_per_beat # ie pulses per quarter note

	for track in mid.tracks:
		for msg in track:
			if msg.type == 'note_off' or (msg.type == 'note_on' and msg.veloctiy==0):
				# (note_off is equivalent to note_on with 0 velocity)
				# (note that midi files can play notes then leave a brief rest before the next note
				#  which isn't explicitly marked as a rest)
				#print msg.velocity, msg.note, msg.time

			elif msg.type == 'note_on':
				#print msg.velocity, msg.note, msg.time
				# default: velocity 64, otherwise 0
				# note: between 0 and 127 inclusively where 60 is middle C (40th note on piano),
				#       A0 is 21, and C8 is 108
				# time: specifies how much you wait before playing this note next
				#       eg. time=0 means you play it immediately as you get the message
				#       the units are ticks

			elif msg.type == 'program_change':
				#print msg.program # instrument
				# 1: acoustic grand piano
				# 2-6: other piano types
				#print msg.channel
				# channel where the instrument is used (10 is supposed to be for precussion?)

			elif msg.type == 'key_signature':
				#print msg.key_signature
				# can be 'Dbm' for D flat minor
				# default 'C' for C major

			elif msg.type == 'time_signature':
				#print msg.numerator, msg.denominator, msg.clocks_per_click
				#print msg.notated_32nd_notes_per_beat
				# default 4, 4, 24, 8
				chEq(msg.clocks_per_click, 24, "clocks_per_tick")
				chEq(msg.notated_32nd_notes_per_beat, 8, "notated_32nd_notes_per_beat")

			elif msg.type == 'set_tempo':
				#print msg.set_tempo
				# possible: 0 ... 16777215
				# default: 500 000
				# this means 500 000 microseconds (0.5 s) per beat (quarter note)
				# thus the default is 120 BMP (beats per minute)
	
	return notes