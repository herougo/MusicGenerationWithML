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
        i = nextDifferent(arr, i)
        
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
        self.n_bars = song.pulse_len / SIXTEENTH_BAR_LEN
        
        # melody
        melody = [REST] * SIXTEENTH_BAR_LEN * self.n_bars
        for note, ti in zip(song.melody, song.melody_intervals):
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
            while end <= melody_arr_len and np.all(melody_arr[start:end] == -2):
                start += SIXTEENTH_BAR_LEN
                end += SIXTEENTH_BAR_LEN
            
            if end > melody_arr_len:
                return result

            # find maximal streak of consecutive non-empty bars
            while (end <= melody_arr_len 
                   and (not np.all(melody_arr[end - SIXTEENTH_BAR_LEN:end] == -2))):
                end += SIXTEENTH_BAR_LEN
            end -= SIXTEENTH_BAR_LEN

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
        chord_ranges = getSatisfyingRanges(self._isPartOfChord, self.chords_arr)
        melodies = map(lambda r: self.melody_arr[r], chord_ranges)
        chords = map(lambda r: self.chords_arr[r[0]], chord_ranges)
        section_lengths = map(lambda r: r[1] - r[0], chord_ranges)
        return zip(melodies, chords, section_lengths)

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




