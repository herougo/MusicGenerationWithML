import numpy as np
import sys
if '..' not in sys.path:
    sys.path.append('..')
from util.other_util import filterNonnegative, nonnegativeIndices, skewness

# Assume we have array of size 5*4*16 = 320 sixteenth note beats
def extractFeatures(key, sixteenth_arr, chord_arr):
	# assume we have *********************
    filtered_note_arr = filterNonnegative(sixteenth_arr)
    filtered_note_indices = nonnegativeIndices(sixteenth_arr)

    filtered_note_abs_diff = np.abs(np.diff(filtered_note_arr))

    features = {}
    features["total_melody_distance"] = totalMelodyDistance(filtered_note_abs_diff)
    features["total_leap_distance"] = totalLeapDistance(filtered_note_abs_diff)
    features["interval_distance_median"] = intervalDistanceMedian(filtered_note_abs_diff)

    features["max_note_break"] = max(np.abs(np.diff(filtered_note_indices)))



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

# ###################################
# Helper Functions ##################
# ###################################

def totalMelodyDistance(filtered_note_abs_diff):
    return np.sum(filtered_note_abs_diff)

def totalLeapDistance(filtered_note_abs_diff):
	diff = filter(lambda x : x >= LEAP_MIN_DIFF, filtered_note_abs_diff)
	return np.sum(diff)

def intervalDistanceMedian(filtered_note_abs_diff):
	return np.median(filtered_note_abs_diff)



''' Planned Features
number of notes fitting chord
number of non-chord tones
proportion of chord-fitting notes
uses minor 3-2-1
uses minor 6-5
minor high distance low
non-leap percentage
last note in key
long notes in key
long note tonic (or 3rd) of key
percentage of non-chord tones that resolve stepwise to inside the chord
percentage of non-chord notes which came stepwise from a chord tone
longest break between notes
last bar in phrase
is tonic (or 3rd or 5th) of current chord reached
is IV chord
# changes in direction
max interval
count 7th of chord as part of chord
number of distinct pitches (ie high C and low C count as different pitches))
Skew of sorted pitch distribution of used pitches
Proportion in chord
Dot product of intervals and proportion
Final note is tonic
Interval between next note divided by current note duration
proportion of notes starting on the quarter note or eight note
Median of interval sizes
321, 31, 43, 65, proportion of 7, 1, 3, 4
proportion of beats on beat vs eighth vs sixteenth
rest in the beginning
'''