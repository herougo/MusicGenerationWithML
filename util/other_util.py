import numpy as np

# Check Equal: Assert that 2 arguments are equal. If they are not raise an exception with a error type
def chEq(x, y, error_type):
	if x != y:
		message = "{} error: {} != {}".format(error_type, x, y)
		raise Exception(message)

# Check Greater than or Equal to
def chGe(x, y, error_type):
	if x < y:
		message = "{} error: {} < {}".format(error_type, x, y)
		raise Exception(message)

# Check Greater than or Equal to
def chLe(x, y, error_type):
	if x > y:
		message = "{} error: {} > {}".format(error_type, x, y)
		raise Exception(message)

def chNotIn(val, my_collection, error_type):
	if val in my_collection:
		message = "{} error: {} in {}".format(error_type, val, my_collection)
		raise Exception(message)

def chIn(val, my_collection, error_type):
	if val not in my_collection:
		message = "{} error: {} not in {}".format(error_type, val, my_collection)
		raise Exception(message)

def filterNonnegative(arr):
	return filter(lambda x: x >= 0, arr)

def nonnegativeIndices(arr):
	return [i for i, val in enumerate(arr) if val >= 0]

def skewness(arr):
	arr_mean = np.mean(arr)
	arr_len = len(arr)
	numerator = np.power(arr - arr_mean, 3) / arr_len
	denominator = np.power(arr - arr_mean, 2) / arr_len
	denominator = np.power(np.sqrt(denominator), 3)

# Purpose: return k numbers from a random permutation of [0, ... n-1]
def sampleSubset(n, k, weights=[]):
	if len(weights) == 0:
		return np.random.choice(n, k, replace=False)
	else:
		return np.random.choice(n, k, replace=False, p=weights)

def itemGetter(index):
	return lambda x : x[index]

# Purpose: sort list of lists by the value in the specified index
def sortUsingIndex(arr, index=0):
	return sorted(arr, key=itemGetter(index))

def intRoundUp(n, mod):
	return ((n + mod - 1) / mod) * mod
