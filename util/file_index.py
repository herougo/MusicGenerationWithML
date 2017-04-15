import os
import csv
import numpy as np

class FileIndex:
    def __init__(self, input_dir='data/midi/', index_dir='data/', file_name='MUSICFILEINDEX.csv'):
        self.input_dir = input_dir
        self.index_path = os.path.join(index_dir, file_name)
        if not os.path.isfile(self.index_path):
            print os.path.abspath(self.index_path)
            with open(self.index_path, "wb") as f:
                writer = csv.writer(f)
                writer.writerow(["entry", "file1"])
                print "File", self.index_path, "created"
        else:
            print "File", self.index_path, "exists"
            
    def getMatrix(self):
        result = None
        with open(self.index_path, 'rb') as f:
            reader = csv.reader(f)
            result = list(reader)
        return np.array(result)
    
    def update(self):
        all_files = self._getFilePathsRecursively(self.input_dir)
        matrix = self.getMatrix()
        known_files = matrix[1:, 1:].flatten()
        missing_files = [f for f in all_files if f not in known_files]
        
        row_counter = len(matrix) - 1
        matrix = list(matrix)
        
        for missing_file in missing_files:
            matrix.append([row_counter, missing_file])
            row_counter += 1
            print "File", missing_file, "added"
            
            self._writeCsv(matrix)
            print "File", self.index_path, "is done updating"
        
        
    def _writeCsv(self, mat):
        with open(self.index_path, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(mat)
            
    def _getFilePathsRecursively(self, directory):
        result = []
        for paths, subdirs, files in os.walk(directory):
            for file in files:
                pure_path = os.path.join(paths, file)
                if pure_path.endswith('.midi') or pure_path.endswith('.mid'):
                    result.append(pure_path)
        return np.array(result)