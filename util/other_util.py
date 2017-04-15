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
	return numerator / denominator

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

# Purpose: find index of the next value in the array that is different from l[i]
def nextDifferent(l, i):
	l_len = len(l)
	val = l[i]

	i += 1
	if i >= l_len:
		return i

	while i < l_len and l[i] == val:
		i += 1

	return i

def randomPartition(n, r):
	partition = [0] * r
	for i in range(n):
		partition[np.random.randint(r)] += 1
	
	return partition

# Purpose: choose a random combination of r items from 0, ... n-1
# Note: this is not uniformly random
def randomCombination(n, r):
	#chGe(r, n, "randomCombination")
	# divide [0, n-1] into r+1 sections
	partition = [0] + [1] * (r-1) + [0]
	for i in range(n-r):
		partition[np.random.randint(r + 1)] += 1
	
	return np.cumsum(partition[:r])

# Purpose: takes a boolean (or binary) array as input and returns the 
# maximal ranges in [a, b) form where the elements are True (or 1)
def boolArrayToRanges(arr):
	building_range = False
	start = 0
	result = []
	for i in range(len(arr)):
		if (not arr[i]) and building_range:
			result.append([start, i])
			building_range = False
		elif arr[i] and (not building_range):
			building_range = True
			start = i
	
	if building_range:
		result.append([start, len(arr)])
	
	return result

# Purpose: get the maximal ranges (similar to boolArrayToRanges) st the 
# element-wise function ("fn") value is true
def getSatisfyingRanges(fn, l):
	arr = map(fn, l)
	return boolArrayToRanges(arr)

def randomSignSwitch(l):
	result = list(l)
	for i in range(len(result)):
		if np.random.randint(2) == 0:
			result[i] *= -1
	return result



	