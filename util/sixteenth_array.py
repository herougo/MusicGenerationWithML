from music_parsing import Song
import numpy as np
from other_util import *

PLACEHOLDER = -3
REST = -2
SUSTAIN = -1
SIXTEENTH_BAR_LEN = 4 * 4

def pulseToSixteenth(n_pulses, ppqn):
    return int((n_pulses * 4) / ppqn)

def sixteenthToPulse(n_sixteenths, ppqn):
    return int((n_sixteenths * ppqn) / 4)

def sixteenthToTimeIntervalFormat(arr, ppqn):
    arr_len = len(arr)
    
    prev_val = None
    prev_start = 0
    
    values = []
    time_intervals = []
    
    i = 0
    while i < arr_len:
        current = arr[i]
        if current == REST:
            if prev_val != None:
                values.append(prev_val)
                time_intervals.append([prev_start, sixteenthToPulse(i, ppqn)])
                prev_val = None
        elif current == SUSTAIN:
            pass
        else:
            if prev_val != None:
                values.append(prev_val)
                time_intervals.append([prev_start, sixteenthToPulse(i, ppqn)])
            prev_val = current
            prev_start = sixteenthToPulse(i, ppqn)
        i += 1

    if prev_val != None:
        values.append(prev_val)
        time_intervals.append([prev_start, sixteenthToPulse(i, ppqn)])
        
    return values, time_intervals

# -3: placeholder
# -2: rest
# -1: sustain previous note
# >= 0: midi note
class SixteenthArray:
    def __init__(self):
        self.melody_arr = []
        self.chords_arr = []
        self.bpm = 120
        self.time_sig = [4, 4]
        self.key_sig = 'C'
        self.n_bars = 0
    
    def loadFromSong(self, song):
        self.bpm = song.bpm
        self.time_sig = list(song.time_sig)
        self.key_sig = song.key_sig
        self.n_bars = pulseToSixteenth(song.pulse_len, song.ppqn) / SIXTEENTH_BAR_LEN
        
        # melody
        melody = [REST] * SIXTEENTH_BAR_LEN * self.n_bars
        for note, ti in zip(song.melody, song.melody_time_intervals):
            start = pulseToSixteenth(ti[0], song.ppqn)
            end = pulseToSixteenth(ti[1], song.ppqn)
            
            melody[start] = note
            for i in range(start + 1, end):
                melody[i] = SUSTAIN
        self.melody_arr = melody
        
        # chords
        chords = [REST] * SIXTEENTH_BAR_LEN * self.n_bars
        for chord, ti in zip(song.chords, song.chord_time_intervals):
            start = pulseToSixteenth(ti[0], song.ppqn)
            end = pulseToSixteenth(ti[1], song.ppqn)
            
            chords[start] = chord
            for i in range(start + 1, end):
                chords[i] = SUSTAIN
        self.chords_arr = chords
        
        
    def toSong(self):
        song = Song()
        song.loadFromSixteenthArray(self)
        return song
        

    def loadFromArguments(self, melody_arr, chords_arr, key_sig="C", bpm = 120, time_sig = [4, 4]):
        chEq(len(melody_arr), len(chords_arr), "loadFromArguments equal array sizes")
        self.melody_arr = melody_arr
        self.chords_arr = chords_arr
        self.bpm = bpm
        self.time_sig = time_sig
        self.key_sig = key_sig
        self.n_bars = (len(self.melody_arr) + SIXTEENTH_BAR_LEN - 1) / SIXTEENTH_BAR_LEN
    
    def splitBars(self):
    	result = []
    	for i in range(0, len(self.melody_arr), SIXTEENTH_BAR_LEN):
    		bar_sixteenth_arr = SixteenthArray()
    		bar_sixteenth_arr.loadFromArguments(
    			self.melody_arr[i:i+SIXTEENTH_BAR_LEN],
    			self.chords_arr[i:i+SIXTEENTH_BAR_LEN],
    			key_sig=self.key_sig, bpm=self.bpm, time_sig=self.time_sig)
    		result.append(bar_sixteenth_arr)
    	return result

    # output: array of SixteenthArrays corresponding to splitting the SixteenthArray
    # by full bars of rest in the melody
    def splitByBarRest(self):
        melody_arr = self.melody_arr
        melody_arr_len = len(self.melody_arr)
        start = 0
        end = SIXTEENTH_BAR_LEN

        result = []

        while True:
            # ignore rest
            while end <= melody_arr_len and np.all(np.array(melody_arr[start:end]) == REST):
                start += SIXTEENTH_BAR_LEN
                end += SIXTEENTH_BAR_LEN
            
            if end > melody_arr_len:
                return result

            # find maximal streak of consecutive non-empty bars
            while (end <= melody_arr_len 
                   and np.any(np.array(melody_arr[end - SIXTEENTH_BAR_LEN:end]) != REST)):
                end += SIXTEENTH_BAR_LEN
            end -= SIXTEENTH_BAR_LEN
        
            chGt(end, start, "splitByBarRest")

            new_sixteenth_arr = SixteenthArray()
            new_sixteenth_arr.loadFromArguments(
                self.melody_arr[start:end], 
                self.chords_arr[start:end], 
                self.key_sig, self.bpm, self.time_sig)
            result.append(new_sixteenth_arr)

            start = end
            end = start + SIXTEENTH_BAR_LEN
    
    def _isPartOfChord(self, val):
        try: # is val an integer?
            val_int = int(val)
            return val_int == SUSTAIN
        except:
            return True
    
    def iterByChord(self):
        melody, melody_intervals = sixteenthToTimeIntervalFormat(self.melody_arr, 4)
        chords, chord_intervals = sixteenthToTimeIntervalFormat(self.chords_arr, 4)
        
        #melody, melody_intervals = [1, 2, 3, 4], [[1, 3], [3, 5], [5, 6], [6, 8]]
        #chords, chord_intervals = [1, 2, 3, 4], [[2, 4], [4, 6], [6, 8], [8, 10]]
        
        melody_len = len(melody)
        chord_len = len(chords)
        
        chord_melodies = []
        chord_melody_intervals = []
        melody_ptr = 0
        
        i = 0
        while i < chord_len:
            chord_start = chord_intervals[i][0]
            chord_end = chord_intervals[i][1]
            
            # go to next note played during the chord
            while melody_ptr < melody_len and melody_intervals[melody_ptr][1] <= chord_start:
                melody_ptr += 1
                
            # while current note is in the chord time frame
            chord_notes = []
            chord_note_intervals = []
            while melody_ptr < melody_len and melody_intervals[melody_ptr][0] < chord_end:
                chord_notes.append(melody[melody_ptr])
                chord_note_intervals.append(list(melody_intervals[melody_ptr]))            
                melody_ptr += 1
            melody_ptr -= 1
            
            chord_melodies.append(chord_notes)
            chord_melody_intervals.append(chord_note_intervals)
            
            i += 1
        
        return chord_melodies, chord_melody_intervals, chords, chord_intervals

    def printMe(self):
        for melody, chord in zip(
            np.array(self.melody_arr).reshape((-1, 16)),
            np.array(self.chords_arr).reshape((-1, 16))):
            print melody, len(melody)
            print " ", chord, len(chord)
            print ""

# Purpose: find index which is not REST
def getMusicStart(arr):
    for i in range(len(arr)):
        if arr[i] != REST:
            return i
    return -1

# Purpose: Find first non-REST value and fill R later REST values as SUSTAIN
def fillSustain(arr):
    arr = list(arr)
    music_start = getMusicStart(arr)

    if music_start != -1:
        for i in range(music_start, len(arr)):
            if arr[i] == REST:
                arr[i] = SUSTAIN

    return arr




