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

# Assumptions:
# - measure distance using the semitone interpretation
# - step is defined as a distance less than 3 semitones
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

    features["interval_skewness"] = skewness(filtered_note_abs_diff)
    features["is_major"] = 1 if 'm' in sixteenth_arr.key_sig else 0
    features["n_notes"] = len(filtered_note_arr)
    
    # Scale Dependent
    features["max_note_break"] = max(np.abs(np.diff(filtered_note_indices)))
    features["start_rest_len"] = float(filtered_note_indices[0]) / 4
    features["pickup_beat_len"] = float((SIXTEENTH_BAR_LEN - filtered_note_indices[0]) % SIXTEENTH_BAR_LEN) / 4
    if filtered_note_len > 1:
        interval_duration_ratios = map(lambda r: r[1] / r[0], zip(filtered_note_abs_diff, filtered_note_durations))
        features["max_interval_duration_ratio"] = max(interval_duration_ratios)
    else:
        features["max_interval_duration_ratio"] = 0
    features["n_bars"] = sixteenth_arr.n_bars


    ***features["tonic_as_final_note"] = (1 if filtered_note_arr[-1] == 1 else 0)

    # Chord Features
    chord_iteration = sixteenth_arr.iterByChord()
    features["ratio_notes_fitting_chord"] = 0.0
    features["ratio_non_ct_step_from_ct"] = 0.0
    features["ratio_non_ct_step_to_ct"] = 0.0
    features["ratio_tonic_of_chord_reached"] = 0.0
    features["ratio_ct_reached"] = 0.0
    features["ratio_longest_note_in_chord"] = 0.0

    features["ratio_notes_fitting_chord_w_duration"] = 0.0
    features["last_note_in_chord"] = 0

    prev_note = -100
    for notes, note_intervals, chord, chord_interval in chord_iteration:
        longest_note_index = np.argmax(map(lambda x: x[1] - x[0], note_intervals))
        features["ratio_longest_note_in_chord"] += chord.fitChord(notes[longest_note_index])

        n_chord_tones = 0

        for note, note_interval in zip(notes, note_intervals):




    return features




# ###################################
# Global Constants ##################
# ###################################

LEAP_MIN_DIFF = 3
MINOR_KEY_NOTE_SEQUENCES = [
    [5, 6], [6, 5],
    [3, 1], [4, 3], [3, 4],
    [5, 7], [7, 5]
]

# 3-2-1 vs. 4-3-1


''' Planned Features
Chord Features
- number of notes fitting chord
- proportion of chord-fitting notes
- last note in key
- long notes in key
  - ratio to chords
- long note tonic (or 3rd) of key
- percentage of non-chord tones that resolve stepwise to inside the chord
- percentage of non-chord notes which came stepwise from a chord tone
- is tonic (or 3rd or 5th) of current chord reached
  - ratio to chords

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
- skew of interval sizes
- is_major

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


