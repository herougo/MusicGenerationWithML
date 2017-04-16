import numpy as np
import sys
if '..' not in sys.path:
    sys.path.append('..')
#from util.other_util import filterNonnegative, nonnegativeIndices, skewness, numDirectionChanges
from util.other_util import *
from util.sixteenth_array import SixteenthArray

self.melody_arr = []
        self.chords_arr = []
        self.bpm = 120
        self.time_sig = [4, 4]
        self.key_sig = 'C'
        self.n_bars = 0

def extractFeatures(sixteenth_arr):
	# assume we have *********************
    filtered_note_arr = filterNonnegative(sixteenth_arr)
    filtered_note_indices = nonnegativeIndices(sixteenth_arr)
    filtered_note_len = len(filtered_note_arr)

    chGt(filtered_note_len, 0)

    filtered_note_abs_diff = np.abs(np.diff(filtered_note_arr))
    filtered_leap_arr = getLeaps(filtered_note_abs_diff)

    

    features = {}
    # Time Independent
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
    
    # Time Dependent
    features["max_note_break"] = max(np.abs(np.diff(filtered_note_indices)))
    features["start_rest_len"] = filtered_note_indices[0]



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

uses minor 3-2-1
uses minor 6-5
non-leap percentage
last note in key
long notes in key
long note tonic (or 3rd) of key
percentage of non-chord tones that resolve stepwise to inside the chord
percentage of non-chord notes which came stepwise from a chord tone
last bar in phrase
is tonic (or 3rd or 5th) of current chord reached
is IV chord
count 7th of chord as part of chord
number of distinct pitches (ie high C and low C count as different pitches))
Skew of sorted pitch distribution of used pitches
Proportion in chord
Final note is tonic
Interval between next note divided by current note duration
proportion of notes starting on the quarter note or eight note
321, 31, 43, 65, proportion of 7, 1, 3, 4
proportion of beats on beat vs eighth vs sixteenth
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


