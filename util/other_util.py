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

def chNotIn(val, my_collection, error_type):
	if val in my_collection:
		message = "{} error: {} in {}".format(error_type, val, my_collection)
		raise Exception(message)

def chIn(val, my_collection, error_type):
	if val not in my_collection:
		message = "{} error: {} not in {}".format(error_type, val, my_collection)
		raise Exception(message)