#encoding=utf8
class UnitInterpreter:

	def i_print(self, tree, env):
		for item in tree:
			self.display(self.interpret(item, env))
	def i_println(self, tree, env):
		for item in tree:
			self.display(self.interpret(item, env), False)
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

		if operator == u'छ':
			return self.interpret(tree[3], env)
		elif operator == u'छैन':
			return not self.interpret(tree[3], env)

	def i_increment(self, tree, env):
		operator = tree[2]
		lhs = self.interpret(tree[4], env)
		iden = self.env_lookup(tree[3], env)

		if operator == '+=':
			self.env_update(env, tree[3], iden + lhs)
		elif operator == '-=':
			self.env_update(env, tree[3], iden - lhs)
		elif operator == '*=':
			self.env_update(env, tree[3] , iden * lhs)
		elif operator == '/=':
			self.env_update(env, tree[3], iden / lhs)

	def i_return(self, tree, env):
		value = self.interpret(tree[1], env)
		raise ReturnException('functionReturn', value)


	def i_slif(self, tree, env):
		if self.interpret(tree[2], env):
			self.interpret(tree[3], env)
		else:
			if tree[4]:	self.interpret(tree[4], env)

	def i_mlif(self, tree, env):
		if self.interpret(tree[2], env):
			self.interpret(tree[3], env)
		else:
			if tree[4]:
				for elblock in tree[4]:
					tag = elblock[0]

					if tag == 'else-if':
						if self.interpret(elblock[2]):
							self.interpret(elblock[3])
							break	# so that only single branch is executed
					elif tag == 'else':
						self.interpret(elblock[2])
						break


	def i_forloop(self, tree, env):
		pre = self.interpret(tree[3], env)
		post = self.interpret(tree[4], env)

		self.add_to_env(env, tree[2], pre)

		while self.env_lookup(tree[2], env) != post:
			self.interpret(tree[6], env)
			pre = self.env_lookup(tree[2], env) + self.interpret(tree[5], env)
			self.env_update(env, tree[2], pre)

	def i_whileloop(self, tree, env):
		expr = self.interpret(tree[2], env)

		while expr:
			self.interpret(tree[3], env)
			expr = self.interpret(tree[2], env)

	def i_repeatloop(self, tree, env):
		iter = self.interpret(tree[2], env)

		for i in xrange(iter):
			self.interpret(tree[3], env)

	def i_functiondef(self, tree, env):
		fname 	= tree[2]
		fparams	= tree[3]
		fbody	= tree[4]
		fvalue	= ('function', fparams, fbody, env)
		self.add_to_env(env, fname, fvalue)

	def i_functioncall(self, tree, env, depth=-1, globalenv = None):
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
			return self.i_fcall_function(fvalue, args, env)
		elif ftype == 'class':
			return self.i_fcall_objinit(fvalue, args, env)

		
	def i_fcall_function(self, fvalue, args, env):
		fparams = fvalue[1]
		fbody	= fvalue[2]
		fenv	= fvalue[3]

		if len(args) != len(fparams):
			self.display('invalid number of params')
			return

		newenv = (fenv, {})
		for i in range(len(args)):
			argval = self.interpret(args[i], env)
			(newenv[1])[fparams[i]] = argval

		try:
			self.interpret(fbody, newenv)
		except ReturnException as e:
			return e.returnval

	def i_fcall_objinit(self, classrep, args , env):
		cenv = classrep[1]

		fvalue = self.env_lookup(u'रचना', cenv, depth=1)
		
		objenv = (cenv, {})

		if fvalue != 'undefined' and fvalue:
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
		
		ovalue = ('object', objenv)
		return ovalue
		# self.add_to_env(env, )

	def i_reference(self, tree, env):
		tempenv = env

		item = tree[2][0]
		if item[0] == 'identifier': 				# search upto global scope
			retobj = self.env_lookup(item[2], tempenv, depth=-1)
		elif item[0] == 'functioncall':
			retobj = self.i_functioncall(item, tempenv, depth=-1)
		
		for item in tree[2][1:]:
			if type(retobj) is tuple:
				if retobj[0] != 'object':
					self.display('Error!! ' + retobj[0] + 'cannot be referenced')
					exit(-1)

				tempenv = retobj[1]
			else:
				tempenv = (None, {})

			if item[0] == 'identifier': 				# search upto class level
				retobj = self.env_lookup(item[2], tempenv, depth=2)
			elif item[0] == 'functioncall':
				retobj = self.i_functioncall(item, tempenv, depth=2, globalenv=env)

		return retobj



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

		cvalue = ('class', cenv)
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
	

	def report_error(self, msg):
		# print "ERROR!! " + msg;
		# exit(0)
		pass

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