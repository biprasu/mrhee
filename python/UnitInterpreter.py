#encoding=utf8
from RheeTypeCheck import RheeTypeCheck
from InterpreterLibrary import checklibrary, call

class UnitInterpreter(RheeTypeCheck):

	def i_assign(self, tree, env):
		refernc = tree[2]

		if (refernc[0] == 'functioncall'):
			self.error("Function can not be assigned", tree[1])
			return
		elif (refernc[0] == 'identifier'):
			self.add_to_env(env, refernc[2], self.interpret(tree[3], env))
		elif ( refernc[0] == 'reference'):
			self.i_reference(refernc, env, self.interpret(tree[3], env), True)
		elif (refernc[0] == 'aryreference'):
			self.i_aryassign(refernc, env, self.interpret(tree[3], env))
		
	def i_print(self, tree, env):
		for item in tree:
			evalexp = self.interpret(item, env)
			self.display(self.e_print(evalexp))
	def i_println(self, tree, env):
		for item in tree:
			evalexp = self.interpret(item, env)
			self.display(self.e_print(evalexp), False)
		self.display('')

	def i_input(self, alist, env):
		# @TODO check for atleast one identifier -> warning!!
		for item in alist:
			tag = item[0][0]

			if tag == 'identifier':
				self.env_update(env, item[0][2], self.get_input())
			else:
				self.i_print([[item[0],]], env)

	def i_arithop(self, tree, env):
		operator = tree[2]

		lhs = self.interpret(tree[3], env)
		rhs = self.interpret(tree[4], env)

		self.e_arithop(lhs, operator, rhs, tree[1])
		if type(lhs) in [str, unicode]:	rhs = str(rhs)
		
		if type(lhs) is tuple:
			return ("array",lhs[1]+rhs[1])

		if operator == '+':
			return lhs + rhs
		elif operator == '-':
			return lhs - rhs
		elif operator == '*':
			return lhs * rhs
		elif operator == '/':
			return lhs / rhs
		elif operator == '%':
			return lhs % rhs
		elif operator == '^':
			return pow(lhs, rhs)


	def i_binop(self, tree, env):
		operator = tree[2]

		lhs = self.interpret(tree[3], env)
		rhs = self.interpret(tree[4], env)

		if (not self.e_binop(lhs, rhs)):
			lhs = self.e_print(lhs)
			rhs = self.e_print(rhs)

		if operator == '>':
			return lhs>rhs
		elif operator == '<':
			return lhs<rhs
		elif operator == '>=':
			return lhs>=rhs
		elif operator == '<=':
			return lhs<=rhs
		elif operator == '==':
			return lhs == rhs
		elif operator == '!=':
			return lhs != rhs
		elif operator == u'र':
			return lhs and rhs
		elif operator == u'वा':
			return lhs or rhs

	def i_negation(self, tree, env):
		operator = tree[2]
		boolexp = self.interpret(tree[3], env)
		boolexp = self.e_boolean(boolexp)

		if operator == u'छ':
			return boolexp
		elif operator == u'छैन':
			return not boolexp

	def i_return(self, tree, env):
		value = self.interpret(tree[1], env)
		raise ReturnException('functionReturn', value)


	def i_slif(self, tree, env):
		evalexp = self.interpret(tree[2], env)
		evalexp = self.e_boolean(evalexp)
		
		if evalexp:
			self.interpret(tree[3], env)
		else:
			if tree[4]:	self.interpret(tree[4], env)

	def i_mlif(self, tree, env):
		evalexp = self.interpret(tree[2], env)
		evalexp = self.e_boolean(evalexp)

		if evalexp:
			self.interpret(tree[3], env)
		else:
			if tree[4]:
				for elblock in tree[4]:
					tag = elblock[0]

					if tag == 'else-if':
						evalexp = self.interpret(elblock[2], env)
						evalexp = self.e_boolean(evalexp)
				
						if evalexp:
							self.interpret(elblock[3], env)
							break	# so that only single branch is executed
					elif tag == 'else':
						self.interpret(elblock[2], env)
						break


	def i_forloop(self, tree, env):
		pre 	= self.interpret(tree[3], env)
		post 	= self.interpret(tree[4], env)
		step 	= self.interpret(tree[5], env)
		refDummy = ("bogus",tree[1],[tree[2],]) if tree[2][0] != 'reference' else tree[2]			# Create ast like reference <laziness>

		self.e_forloop(pre, post, step, tree[1])
		
		self.i_reference(refDummy, env, pre, True)

		while self.i_reference(refDummy, env) != post:
			try:
				self.interpret(tree[6], env)
			except BreakException as e:
				break
			except ContinueException as e1:
				pass
			finally:
				pre = self.i_reference(refDummy, env) + step
				self.i_reference(refDummy, env, pre, True)

	def i_whileloop(self, tree, env):
		expr = self.interpret(tree[2], env)
		expr = self.e_boolean(expr)

		while expr:
			try:
				self.interpret(tree[3], env)
				expr = self.interpret(tree[2], env)
			except BreakException as e:
				break
			except ContinueException as e:
				pass

	def i_repeatloop(self, tree, env):
		iter = self.interpret(tree[2], env)

		if not (type(iter) in [int, float]):
			self.error("Choti iteration only supports integers", tree[1])

		for i in xrange(iter):
			try:
				self.interpret(tree[3], env)
			except BreakException as e:
				break
			except ContinueException as e:
				pass

	def i_functiondef(self, tree, env):
		fname 	= tree[2]
		fparams	= tree[3]
		fbody	= tree[4]
		fvalue	= ('function', fparams, fbody, env, fname)
		self.add_to_env(env, fname, fvalue)

	def i_functioncall(self, tree, env, depth=-1, globalenv = None):
		lineno = tree[1]
		fname = tree[2]
		args  = tree[3]

		fvalue = self.env_lookup(fname, env, depth)

		if fvalue == 'undefined':
			if checklibrary(fname):
				call(fname, args, env)
				return

			self.display('Reference to undefined function!!')
			return

		if globalenv:
			env = globalenv

		ftype = fvalue[0]
		if ftype == 'function':
			return self.i_fcall_function(fvalue, args, env, lineno)
		elif ftype == 'class':
			return self.i_fcall_objinit(fvalue, args, env, lineno)

		
	def i_fcall_function(self, fvalue, args, env, lineno):
		fparams = fvalue[1]
		fbody	= fvalue[2]
		fenv	= fvalue[3]

		if len(args) != len(fparams):
			self.error('Invalid number of params to the function ', lineno)
			return

		newenv = (fenv, {})
		for i in range(len(args)):
			argval = self.interpret(args[i], env)
			(newenv[1])[fparams[i]] = argval

		try:
			self.interpret(fbody, newenv)
		except ReturnException as e:
			return e.returnval
		except TracebackException as te:
			self.error("traceback",lineno,tb=True)

	def i_fcall_objinit(self, classrep, args , env, lineno):
		cenv = classrep[1]

		fvalue = self.env_lookup(u'रचना', cenv, depth=1)
		
		objenv = self.createObjEnv(cenv)

		if fvalue != 'undefined' and fvalue:	# if class has a constructor
			fparams = fvalue[1]
			fbody	= fvalue[2]
			fenv	= fvalue[3]
			print args , fparams
			if len(args) != len(fparams):
				self.display('invalid number of params')
				return

			for i in range(len(args)):
				argval = self.interpret(args[i], env)
				(objenv[1])[fparams[i]] = argval

			try:
				self.interpret(fbody, objenv)
			except ReturnException as e:
				self.display("Returned value is of no value")
			except TracebackException as te:
				self.error("traceback",lineno,tb=True)
		
		ovalue = ('object', objenv, classrep[2])
		return ovalue
		# self.add_to_env(env, )

	def createObjEnv(self, cenv):
		dc = {}
		value = None

		for key in cenv[1]:
			value = cenv[1][key]

			if self.get_type(value) in ["num", "string", "bool", "undefined", "array", "object"]:
				dc[key] = value

		return (cenv, dc)

	def i_reference(self, tree, env, assign=None, aflag=False):
		tempenv = env

		item = tree[2][0]			# first item in chain
		numChain = len(tree[2])

		if item[0] == 'identifier': 				# search upto global scope
			if (numChain == 1 and aflag):
				self.env_update(tempenv, item[2], assign)
			retobj = self.env_lookup(item[2], tempenv, depth=-1)
		
		elif item[0] == 'functioncall':
			if (aflag):
				self.error("Chaining up with function to assign doesn't make sense.", tree[1])
			retobj = self.i_functioncall(item, tempenv, depth=-1)
		
		elif item[0] == 'aryreference':
			if (aflag and numChain == 1 ):
				self.i_aryassign(item, tempenv, assign)
			retobj = self.i_aryreference(item, tempenv)

		
		for item in tree[2][1:]:		# remaining chain
			if type(retobj) is tuple:
				if retobj[0] != 'object':
					self.error(retobj[0] + 'cannot be referenced', tree[1])
					exit(-1)

				tempenv = retobj[1]
			else:
				tempenv = (None, {})

			if item[0] == 'identifier': 				# search upto class level
				if (aflag and item == tree[2][-1]):
					# if assign and is last item
					self.env_update(tempenv, item[2], assign)
				retobj = self.env_lookup(item[2], tempenv, depth=2)
			
			elif item[0] == 'functioncall':
				if (aflag):
					self.error("Chaining up with function to assign doesn't make sense.", tree[1])
				retobj = self.i_functioncall(item, tempenv, depth=2, globalenv=env)
			
			elif item[0] == 'aryreference':
				if (aflag and item == tree[2][-1]):
					self.i_aryassign(item, tempenv, assign)
				retobj = self.i_aryreference(item, tempenv, depth=2)

		
		return retobj

	def i_aryreference(self, tree, env, depth=-1):

		ident = tree[2]
		idata = self.env_lookup(ident[2], env, depth)
		self.e_arraycheck(idata, tree[1])

		indices = tree[3]
		start = None
		end = None

		for item in indices:
			#if idata is not array index error
			start 	= self.interpret(item[2], env)

			if (item[0] == 'normal'):
				self.e_aryref(start, None, len(idata[1]), tree[1])		# typechecking

				idata = idata[1][start]
			else:
				end  = self.interpret(item[2], env)
				
				self.e_aryref(start, end, len(idata[1]), tree[1])
				
				idata = idata[1][start:end]

		if type(idata) is list:
			# it can be object too!! javascript
			return ('array', idata)
		return idata

	def i_aryassign(self, tree, env, assign):
		ident = tree[2]

		indices = tree[3]
		tinx  	= []
		atom	= None

		for item in indices:
			if item[0] == 'arrayslice':
				self.error("Array slice assignment not supported yet", tree[1])
				return

			atom = self.interpret(item[2],env)
			self.e_aryassign(atom, tree[1])					# typechecking
				
			tinx += [atom]

		self.env_update_array(env, ident[2], tinx, assign) 
		return True

			# try:
			# 	self.interpret(item, env)
			# except ReturnException as e:
			# 	if type(e.returnval) is tuple:
			# 		if e.returnval[0] == 'object':
			# 			tempenv = e.returnval[1]
			# 			continue



	def i_classdef(self, tree, env):
		cname = tree[2]
		cbody = tree[3]

		cenv = (env, {})
		self.interpret(cbody, cenv)

		cvalue = ('class', cenv, cname)
		self.add_to_env(env, cname, cvalue)




	map_num = {u'\u0966':'0', u'\u0967':'1', u'\u0968':'2', u'\u0969':'3',
			u'\u096a':'4', u'\u096b':'5', u'\u096c':'6', u'\u096d':'7',
			u'\u096e':'8' ,u'\u096f':'9', u'+':'+', u'-':'-', u'e':'e',
			u'E':'E', u'.':'.', 'a':'a', 'b':'b', 'c':'c', 'd':'d', 'A':'A', 
			'B':'B', 'C':'C', 'D':'D', 'x':'x', 'X':'X',
			}

	def num_mapper(self, num, base=10):
		'Note: Only returns the true value of decimal and float'

		if not ( isinstance(num,str) or isinstance(num,unicode)):
			return num

		ascii = ''
		for char in num:
			if char in self.map_num:
				ascii += self.map_num[char]
			else:
				self.error('Can`t parse the number '+num, );
				return False
		if ascii.find('.') == ascii.find('e') == ascii.find('E') == -1:
			return int(ascii, base)
		else:
			return float(ascii)

	def display(self, content, linebreak=True):
		'''shifting platform should be easy
		'''
		if linebreak:	print content
		else:			print content,

	def get_input(self, content=''):
		return raw_input(content)	# always returns a string version
	

	def error(self, msg, lineno=None, tb=None):
		if not tb:
			print "ERROR!! " + msg + " in line number "+ str(lineno);
		print "SamasyaSuchak: " + str(lineno)

		raise TracebackException("Trace it Back")
		exit(0)
		# pass

a = UnitInterpreter()
# a.test_envlookup()
# a.display("test", True)
# a.display("test", False)
# a.display("test", True)
# a.display("test", True)

class ReturnException(Exception):
	def __init__(self, message, returnval):
		Exception.__init__(self, message)
		self.returnval = returnval

class ContinueException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class BreakException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class TracebackException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)
		