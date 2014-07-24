class RheeTypeError(object):
	"""Type checking and handling errors also final unicode mapping"""
	def __init__(self):
		super(RheeTypeError, self).__init__()

	def e_print(self, bakra):
		'number, string, bool, array'

		collector = u''

		if type(bakra) in [int, float]:		# number
			# map it back to unicode
			return str(bakra)
		elif type(bakra) is bool:			# booleans
			if bakra:
				return 'satya'
			return 'jhuto'
		elif type(bakra) is type(None):
			return "sunya"
			
		elif type(bakra) is list:			# array
			collector = u'['
			
			for item in bakra[:-1]:
				collector += self.e_print(item) + ", "
			collector += self.e_print(bakra[-1]) + u']'
			return collector
		
		elif type (bakra) is tuple:
			if bakra:
				if bakra[0] == 'function':
					return "(function instance of "# + bakra[4] + ")"
				elif bakra[0] == 'object':
					return "(object instance of "# + bakra[2] + ")"
				elif bakra[0] == 'class':	
					return "(class instance of "# + bakra[2] + ")"
		# else it is string
		return bakra

	def e_boolean(self, obj):
		'Everything except empty string, empty array, Null and False is true'
		if type(obj) is type(None):
			return False
		elif type(obj) is bool:
			return obj
		elif type(obj) in [str, unicode] and obj == "":
			return False
		elif type(obj) is list and obj == []:
			return False
		return True

	def e_forloop(self, pre, post, step):
		if type(pre) in [int, float]:
			if type(post) in [int, float]:
				if type(step) in [int, float]:
					return True
		return False

	def e_aryref(self, start, end, arlen):
		if not (type(start) in [int, float]):
			self.error("Array index should be number.")
			return

		if start>=arlen:
			self.error("Array index out of bound")
			return

		if end:
			if not (type(end) in [int, float]):
				self.error("Array index should be number.")
				return

			if end>=arlen:
				self.error("Array index out of bound")
				return
		return
	def e_aryassign(self, indx):
		if not (type(indx) in [int, float]):
			self.error("Array index should be number")
			return

	typeMap = { int 		: 'num',
				float		: 'num',
				str 		: 'string',
				unicode		: 'string',
				list		: 'array',
				bool 		: 'bool',
				type(None)	: 'undefined'
	}

	def e_arithop(self, lhs, operator, rhs):
		'only type of number, string and array are allowed'
		try:
			ltype = type(lhs)
			rtype = type(rhs)

			if (not ltype in self.typeMap) or (not rtype in self.typeMap):
				raise RTypeError("Message for Developer!! arithop "+ltype+" "+operator+" "+rtype)

			ltype = self.typeMap[ltype]
			rtype = self.typeMap[rtype]

			if (ltype == 'num'):
				# if lhs = num, rhs should be num
				if not (rtype == 'num'):
					raise RTypeError("Invalid operation between num and "+rtype)
				
				if operator == '/' and rhs == 0:
					raise RTypeError("DivideByZero: You can't divide number by zero.")
			
			elif (ltype == "string"):
				# if lhs = string
				if (operator != "+"):
					raise RTypeError("Invalid operator "+operator+" for string type")

				if (rtype == 'string' or rtype == 'num'):
					return True

				raise RTypeError("Invalid operation between string and "+rtype)

			elif (ltype == 'array'):
				# if lhs = array
				if rtype == 'array' and operator == '+':
					return True

				raise RTypeError("Invalid operation between array "+operator+" "+rtype)
			else:
				# NULL BOOLS
				# filterout function and object
				if ltype is tuple:
					raise RTypeError(lhs[0] + " cannot be used in arithop")
				elif rtype is tuple:
					raise RTypeError(rhs[0] + " cannot be used in arithop")
				raise RTypeError("Invalid operation with "+ltype+" and "+rtype)
		except RTypeError as e:
			self.error("TypeError: "+e.message)

class RTypeError(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)
		

if __name__ == '__main__':
		test = RheeTypeError()
		print(test.e_print("43"))
		print(test.e_print(43))
		print(test.e_print(43e-3))
		print(test.e_print(43e49))
		print(test.e_print(None))
		print(test.e_print(True))
		print(test.e_print(False))
		print(test.e_print(["43", 43, True, False, [None, 4e67, True]]))
		print(test.e_print(('function', 'fparams', 'fbody', 'fenv', 'fname')))
		print(test.e_print(('object', 'oenv', 'cname')))
		print(test.e_print(('class', 'cenv', 'cname')))

		print("")
		print (test.e_boolean([]))
		print (test.e_boolean(u""))
		print (test.e_boolean(False))
		print (test.e_boolean([34]))
		print (test.e_boolean(None))
		print (test.e_boolean(('object', 'oenv', 'cname')))
		print (test.e_boolean(0))
		print (test.e_boolean(3))