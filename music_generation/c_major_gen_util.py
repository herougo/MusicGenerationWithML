from util.other_util import *
from util.music_theory import *


# 55 is G before C4

POSSIBLE_NOTES = range(5, 20)
# 5 - > 55
# 12 -> 67
# 29 -> 79

MAJOR_MIDI_OFFSET_TO_DEGREE = dict((offset, i+1) for i, offset in enumerate(SUPPORTED_KEY_QUALITIES['+']))

def cMajorMidiNumToScaleDegree(midi_num):
    chGe(midi_num, 55, "cMajorMidiNumToScaleDegree")
    chGe(79, midi_num, "cMajorMidiNumToScaleDegree")
    
    octave = ((midi_num - 48) / 12) * 7
    return MAJOR_MIDI_OFFSET_TO_DEGREE[midi_num % 12] + octave
    

def scaleDegreeToCMajorMidiNum(scale_degree):
    offset = 12 * ((scale_degree - 1) / 7) + 48
    mod = (scale_degree + 6) % 7
    return offset + SUPPORTED_KEY_QUALITIES['+'][mod]

def _tests():
	for i in range(5, 20):
        chEq(cMajorMidiNumToScaleDegree(_toMidiNoteHelper(i)), i, "test1")