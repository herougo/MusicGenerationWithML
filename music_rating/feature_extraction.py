import numpy as np
import sys
if '..' not in sys.path:
    sys.path.append('..')
#from util.other_util import filterNonnegative, nonnegativeIndices, skewness, numDirectionChanges
from util.other_util import *
from util.sixteenth_array import SixteenthArray
from util.music_theory import Harmony

'''
self.melody_arr = []
        self.chords_arr = []
        self.bpm = 120
        self.time_sig = [4, 4]
        self.key_sig = 'C'
        self.n_bars = 0
'''

RL_CHORD = Harmony()

def extractFeatures(sixteenth_arr):
    # assume we have *********************
    filtered_note_arr, filtered_note_durations = sixteenthToTimeIntervalFormat(sixteenth_arr.melody_arr, 4)
    filtered_note_durations = map(lambda r: r[1] - r[0], filtered_note_durations)
    filtered_note_indices = nonnegativeIndices(sixteenth_arr.melody_arr)
    
    filtered_note_len = len(filtered_note_arr)

    chGt(filtered_note_len, 0)

    filtered_note_abs_diff = np.abs(np.diff(filtered_note_arr))
    filtered_leap_arr = getLeaps(filtered_note_abs_diff)

    features = {}
    # Scale Independent
    # - works for any time scale of array (sixteenth vs. eighth)
    features["total_melody_distance"] = totalMelodyDistance(filtered_note_abs_diff)
    features["total_leap_distance"] = np.sum(filtered_leap_arr)
    features["interval_distance_median"] = intervalDistanceMedian(filtered_note_abs_diff)
    features["#_direction_changes"] = numDirectionChanges(filtered_note_arr)
    features["max_interval"] = max(filtered_note_abs_diff)
    features["interval_occurrence_dot_prod"] = intervalOccDotProduct(filtered_note_abs_diff)
    if filtered_note_len > 1:
        features["leap_proportion"] = float(len(filtered_leap_arr)) / (filtered_note_len - 1)
    else:
        features["leap_proportion"] = 0
    features["n_distinct_pitches"] = len(set(filtered_note_arr))
    
    ***features["tonic_as_final_note"] = 1 if filtered_note_arr[-1] == 1 else 0
    
    # Scale Dependent
    features["max_note_break"] = max(np.abs(np.diff(filtered_note_indices)))
    features["start_rest_len"] = filtered_note_indices[0]
    features["pickup_beat_len"] = float((SIXTEENTH_BAR_LEN - filtered_note_indices[0]) % SIXTEENTH_BAR_LEN) / 4
    if filtered_note_len > 1:
        interval_duration_ratios = map(lambda r: r[1] / r[0], zip(filtered_note_abs_diff, filtered_note_durations))
        features["max_interval_duration_ratio"] = max(interval_duration_ratios)
    else:
        features["max_interval_duration_ratio"] = 0



# ###################################
# Global Constants ##################
# ###################################

LEAP_MIN_DIFF = 2
MINOR_KEY_NOTE_SEQUENCES = [
    [5, 6], [6, 5],
    [3, 1], [4, 3], [3, 4],
    [5, 7], [7, 5]
]

# 3-2-1 vs. 4-3-1


''' Planned Features
Chord Features
- number of notes fitting chord
- number of non-chord tones
- proportion of chord-fitting notes
- last note in key
- long notes in key
- long note tonic (or 3rd) of key
- percentage of non-chord tones that resolve stepwise to inside the chord
- percentage of non-chord notes which came stepwise from a chord tone
- is tonic (or 3rd or 5th) of current chord reached
- Proportion in chord

Note Sequences
- uses minor 3-2-1
- uses minor 6-5
- 321, 31, 43, 65, proportion of 7, 1, 3, 4

Bar Features
- is IV chord
- last bar in phrase

Future
- count 7th of chord as part of chord
- Skew of sorted pitch distribution of used pitches
- fits Blues scale


Done ***********

General
- total_melody_distance
- total_leap_distance
- interval_distance_median
- #_direction_changes
- max_interval
- interval_occurrence_dot_prod
- leap_proportion
- n_distinct_pitches
- tonic_as_final_note
- max_note_break
- start_rest_len

Rhythm Features
- max ratio of Interval between next note divided by current note duration
- proportion of beats on beat vs eighth vs sixteenth


'''

# ###################################
# Helper Functions ##################
# ###################################

def totalMelodyDistance(filtered_note_abs_diff):
    return np.sum(filtered_note_abs_diff)

def getLeaps(filtered_note_abs_diff):
    return filter(lambda x : x >= LEAP_MIN_DIFF, filtered_note_abs_diff)

def intervalDistanceMedian(filtered_note_abs_diff):
    return np.median(filtered_note_abs_diff)

def intervalOccDotProduct(filtered_note_abs_diff):
    occ_dict = listToOccDict(filtered_note_abs_diff)
    result = 0
    for k in occ_dict.keys():
        result += k * occ_dict[k]
    return result


