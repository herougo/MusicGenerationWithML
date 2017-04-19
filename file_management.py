from util.file_index import FileIndex
import os

GIT_REPO_PATH = os.path.dirname(os.path.abspath(__file__))

os.chdir(GIT_REPO_PATH)
print "Directory changed to {}".format(GIT_REPO_PATH)

_input_dir = 'data'
_index_dir = 'data'
_file_name = 'MUSICFILEINDEX.csv'

midi_index = FileIndex(_input_dir, _index_dir, _file_name)