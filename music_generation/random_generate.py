import sys
import numpy as np

from util.sixteenth_array import *
from util.other_util import *
from util.music_theory import *
from c_major_gen_util import *


def randomlyGenerateBars1(n_bars):
    melody_arr = [REST] * SIXTEENTH_BAR_LEN * n_bars
    for i in range(8 * n_bars):
        random_note = np.random.randint(5, 20)
        melody_arr[2*i] = scaleDegreeToCMajorMidiNum(random_note)
    
    
    melody_arr = fillSustain(melody_arr)
        
    harmony_arr = [SUSTAIN] * SIXTEENTH_BAR_LEN
    harmony_arr[0] = Harmony('C', '+')
    harmony_arr = harmony_arr * n_bars
    
    result = SixteenthArray()
    result.loadFromArguments(melody_arr, harmony_arr)
    
    return result


    
def randomlyGenerateMelodyBar2():
    # based on bar 1 of Poker Face
    # 6 notes
    # distance 9
    n_notes = min(int(np.random.normal(6, 1)), 8)
    n_notes = max(n_notes, 3)
    distance = max(int(np.random.normal(10, 1)), 3)
    
    eighth_note_indices = randomCombination(8, n_notes)
    eighth_note_differences = randomPartition(distance, n_notes-1)
    eighth_note_differences = randomSignSwitch(eighth_note_differences)
    
    possible_notes_len = len(POSSIBLE_NOTES)
    eighth_notes = np.cumsum([0] + list(eighth_note_differences))
    eighth_notes -= min(eighth_notes)
    eighth_note_max = max(eighth_notes)
    
    chGe(possible_notes_len, eighth_note_max)
    
    first_note = 5 + np.random.randint(0, possible_notes_len - eighth_note_max)
    eighth_notes += first_note
    
    melody_arr = [REST] * SIXTEENTH_BAR_LEN
    for i in range(n_notes):
        note_index = 2 * eighth_note_indices[i]
        midi_note = scaleDegreeToCMajorMidiNum(eighth_notes[i])
        chGe(midi_note, 55)
        chGe(79, midi_note)
        melody_arr[note_index] = midi_note
        
    melody_arr = fillSustain(melody_arr)
    
    return melody_arr

def randomlyGenerateBars2(n_bars):
    melody_arr = []
    for i in range(n_bars):
        melody_arr += randomlyGenerateMelodyBar2()

    harmony_arr = [SUSTAIN] * SIXTEENTH_BAR_LEN
    harmony_arr[0] = Harmony('C', '+')
    harmony_arr = harmony_arr * n_bars
    
    result = SixteenthArray()
    result.loadFromArguments(melody_arr, harmony_arr)
    return result
    
    