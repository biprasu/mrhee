#encoding=utf8
from RheeTypeError import RheeTypeError
class UnitInterpreter(RheeTypeError):

	def i_assign(self, tree, env):
		refernc = tree[2]

		if (refernc[0] == 'functioncall'):
			self.error("Function can not be assigned")
			return
		elif (refernc[0] == 'identifier'):
			self.add_to_env(env, refernc[2], self.interpret(tree[3], env))
		elif ( refernc[0] == 'reference'):
			self.i_reference(refernc, env, self.interpret(tree[3], env))
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

		self.e_arithop(lhs, operator, rhs)
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
		pre = self.interpret(tree[3], env)
		post = self.interpret(tree[4], env)
		step = self.interpret(tree[5], env)

		self.e_forloop(pre, post, step)
		
		self.add_to_env(env, tree[2], pre)

		while self.env_lookup(tree[2], env) != post:
			try:
				self.interpret(tree[6], env)
			except BreakException as e:
				break
			except ContinueException as e1:
				pass
			finally:
				pre = self.env_lookup(tree[2], env) + step
				self.env_update(env, tree[2], pre)

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
			self.error("Choti iteration only supports integers")

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
			self.error('Invalid number of params to the function ' + str(lineno))
			return

		newenv = (fenv, {})
		for i in range(len(args)):
			argval = self.interpret(args[i], env)
			(newenv[1])[fparams[i]] = argval

		try:
			self.interpret(fbody, newenv)
		except ReturnException as e:
			return e.returnval

	def i_fcall_objinit(self, classrep, args , env, lineno):
		cenv = classrep[1]

		fvalue = self.env_lookup(u'रचना', cenv, depth=1)
		
		objenv = (cenv, {})

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
		
		ovalue = ('object', objenv, classrep[2])
		return ovalue
		# self.add_to_env(env, )

	def i_reference(self, tree, env, assign=None):
		tempenv = env

		item = tree[2][0]			# first item in chain
		if item[0] == 'identifier': 				# search upto global scope
			retobj = self.env_lookup(item[2], tempenv, depth=-1)
		elif item[0] == 'functioncall':
			retobj = self.i_functioncall(item, tempenv, depth=-1)
		
		for item in tree[2][1:]:		# remaining chain
			if type(retobj) is tuple:
				if retobj[0] != 'object':
					self.display('Error!! ' + retobj[0] + 'cannot be referenced')
					exit(-1)

				tempenv = retobj[1]
			else:
				tempenv = (None, {})

			if item[0] == 'identifier': 				# search upto class level
				if (assign and item == tree[2][-1]):
					# if assign and is last item
					self.env_update(tempenv, item[2], assign)
				retobj = self.env_lookup(item[2], tempenv, depth=2)
			elif item[0] == 'functioncall':
				if (assign):
					self.error("Chaining up with function to assign doesn't make sense.")
				retobj = self.i_functioncall(item, tempenv, depth=2, globalenv=env)
		
		return retobj

	def i_aryreference(self, tree, env):

		ident = tree[2]
		idata = self.env_lookup(ident[2], env)
		self.e_arraycheck(idata)

		indices = tree[3]
		start = None
		end = None

		for item in indices:
			#if idata is not array index error
			start 	= self.interpret(item[2], env)

			if (item[0] == 'normal'):
				self.e_aryref(start, None, len(idata[1]))		# typechecking

				idata = idata[1][start]
			else:
				end  = self.interpret(item[2], env)
				
				self.e_aryref(start, end, len(idata[1]))
				
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
				self.error("Array slice assignment not supported yet")
				return

			atom = self.interpret(item[2],env)
			self.e_aryassign(atom)					# typechecking
				
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
				self.report_error('Can`t parse the number '+num);
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
	

	def error(self, msg):
		print "ERROR!! " + msg;
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
		