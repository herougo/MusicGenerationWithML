from mido import MidiFile, MidiTrack, Message

def midiToNoteDict(file_name):
	mid = MidiFile(file_name) # a Mozart piece

	notes = []

	time = float(0)
	prev = float(0)

	for msg in mid:
		print msg

		### this time is in seconds, not ticks
		time += msg.time
		if not msg.is_meta:
			### only interested in piano channel
			if msg.channel == 1:
				if msg.type == 'note_on':
					# note in vector form to train on
					data = msg.bytes() 
					# only interested in the note and velocity. note message is in the form of [type, note, velocity]
					note, velocity = data[1:3]
					notes.append([note, time-prev])
					prev = time

	return notes

def noteArrayToMidi(note_array, file_name):
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)

	for note in note_array:
		# 147 means note_on
		note = np.insert(note, 0, 147)
		bytes = note.astype(int)
		print (note)
		msg = Message.from_bytes(bytes[0:3]) 
		time = int(note[3]/0.001025) # to rescale to midi's delta ticks. arbitrary value for now.
		msg.time = time
		track.append(msg)

	mid.save(file_name)

if __name__ == "__main__":
	arr = midiToNoteArray('siraj-music/Blank Space - Chorus.midi')
	print arr