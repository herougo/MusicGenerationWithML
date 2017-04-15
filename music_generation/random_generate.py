import sys
import numpy as np

from util.sixteenth_array import *
from util.other_util import *
from util.music_theory import *


# 55 is G before C4

# Generate C Major

POSSIBLE_NOTES = range(5, 20)
# 5 - > 55
# 12 -> 67
# 29 -> 79


def _toMidiNoteHelper(yo):
    offset = 12 * ((yo - 1) / 7) + 48
    mod = (yo + 6) % 7
    return offset + SUPPORTED_KEY_QUALITIES['+'][mod]


def randomlyGenerateBar1():
    melody_arr = [REST] * SIXTEENTH_BAR_LEN
    for i in range(8):
        random_note = np.random.randint(5, 20)
        melody_arr[2*i] = _toMidiNoteHelper(random_note)
    
    
    melody_arr = fillSustain(melody_arr)
        
    harmony_arr = [SUSTAIN] * SIXTEENTH_BAR_LEN
    harmony_arr[0] = Harmony('C', '+')
    
    result = SixteenthArray()
    result.loadFromArguments(melody_arr, harmony_arr)
    
    return result


    
def randomlyGenerateBar2():
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
    eighth_notes += min(eighth_notes)
    eighth_note_max = max(eighth_notes)
    
    if eighth_note_max >= possible_notes_len:
        raise Exception("randomlyGenerateBar2")
    
    first_note = np.random.randint(0, possible_notes_len - eighth_note_max)
    eighth_notes += first_note
    
    melody_arr = [REST] * SIXTEENTH_BAR_LEN
    for i in range(n_notes):
        note_index = 2 * eighth_note_indices[i]
        melody_arr[note_index] = _toMidiNoteHelper(eighth_notes[i])
        
    melody_arr = fillSustain(melody_arr)
    
    return melody_arr
    
    harmony_arr = [SUSTAIN] * SIXTEENTH_BAR_LEN
    harmony_arr[0] = Harmony('C', '+')
    
    result = SixteenthArray()
    result.loadFromArguments(melody_arr, harmony_arr)
    return result
    
    