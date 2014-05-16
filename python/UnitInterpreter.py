#encoding = UTF8
class UnitInterpreter:

	def i_print(self, tree, env):
		for item in tree:
			print self.interpret(item, env)


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









	map_num = {u'\u0966':'0', u'\u0967':'1', u'\u0968':'2', u'\u0969':'3',
			u'\u096a':'4', u'\u096b':'5', u'\u096c':'6', u'\u096d':'7',
			u'\u096e':'8' ,u'\u096f':'9', u'+':'+', u'-':'-', u'e':'e',
			u'E':'E', u'.':'.',
			}

	def num_mapper(self, num):
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
			return int(ascii)
		else:
			return float(ascii)

	def env_lookup(self, vname, env):
		if vname in env[1]:
			return (env[1])[vname]
		elif env[0] == None:
			print 'undefined variable ' + vname
			raise NameError
		else:
			return self.env_lookup(vname, env[0])




	def test_envlookup(self):
		env = (None, {'a':3, 'er':'tes'})
		newenv = (env, {'a':6, 'r':34, 'rest':'ters'})
		newenv2 = (newenv, {'a':5, 'w':567, 'ew':'ksli'})
		print self.env_lookup('a', newenv)
		print self.env_lookup('er', newenv2)
		print self.env_lookup('ewer', newenv2)

	def report_error(self, msg):
		# print "ERROR!! " + msg;
		# exit(0)
		pass

# a = UnitInterpreter()
# a.test_envlookup()