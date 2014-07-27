#encoding=utf8

from UnitInterpreter import UnitInterpreter
from UnitInterpreter import ContinueException, BreakException

class RheeInterpreter(UnitInterpreter):
	"""docstring for RheeInterpreter"""

	environment = (None,{})

	def interpret(self, trees, env = None):
		if not env:	env = self.environment

		for tree in trees:
			if not tree:	continue

			stmt 	= tree[0]
			lineno 	= tree[1]

			#@ dictionary based lambda function
			if stmt == 'decimal':
				return self.num_mapper(tree[2])
			elif stmt == 'octal':
				return self.num_mapper(tree[2], 8)
			elif stmt == 'hexa':
				return self.num_mapper(tree[2], 16)
			elif stmt == 'float':
				return self.num_mapper(tree[2])
			elif stmt == 'imaginary':
				pass
			elif stmt == 'string':
				return tree[2]
			elif stmt == 'null':
				return None
			elif stmt == 'true':
				return True
			elif stmt == 'false':
				return False
			elif stmt == 'array':
				return ("array", [self.interpret(t) for t in tree[2]])
			elif stmt == 'identifier':
				return self.env_lookup(tree[2], env)
			elif stmt == 'functioncall':
				return self.i_functioncall(tree, env)
			elif stmt == 'reference':
				return self.i_reference(tree, env)
			elif stmt == 'aryreference':
				return self.i_aryreference(tree, env)
			elif stmt == 'unaryminus':
				return -1 * self.interpret(tree[2], env)
			elif stmt == 'arithop':
				return self.i_arithop(tree, env)
			elif stmt == 'paranthesis':
				return self.interpret(tree[2], env)
			elif stmt == 'binop':
				return self.i_binop(tree, env)
			elif stmt == 'negation':
				return self.i_negation(tree,env)
			elif stmt == 'expression':	# @ return
				self.interpret(tree[2], env)
			elif stmt == 'assign':
				self.i_assign(tree, env)
			elif stmt == 'print':
				self.i_print(tree[2], env)
			elif stmt == 'println':
				self.i_println(tree[2], env)
			elif stmt == 'input':
				self.i_input(tree[2], env)
			elif stmt == 'return':  #?
				self.i_return(tree, env)
			elif stmt == 'continue':
				raise ContinueException("continue")
			elif stmt == 'break':
				raise BreakException("Break")
			elif stmt == 'slif':
				self.i_slif(tree, env)
			elif stmt == 'mlif':
				self.i_mlif(tree, env)
			elif stmt == 'forloop':
				self.i_forloop(tree, env)
			elif stmt == 'whileloop':
				self.i_whileloop(tree, env)
			elif stmt == 'repeatloop':
				self.i_repeatloop(tree, env)
			elif stmt == 'functiondef':
				self.i_functiondef(tree, env)
			elif stmt == 'classdef':
				self.i_classdef(tree, env)
			elif stmt == 'SyntaxError':
				self.display('SyntaxError!! '+tree[2]+ " on line " + str(lineno))
			else:
				self.display('unimplemented handle for ' + tree)



	def add_to_env(self, env, vname, value):
		(env[1])[vname] = value
	def env_update(self, env, vname, value):	# @TODO get detail about the variable scope management
		(env[1])[vname] = value
		return True
	def env_update_array(self, env, vname, indx, value):
		temp = (env[1])[vname]
		
		for i in indx[:-1]:
			if i>len(temp[1]):
				self.error("Array index out of bound")
				return
			if type(temp) != tuple and type(temp) != unicode :
				self.error("Cannot access non array element with index")

			temp = temp[1][i]
		temp[1][indx[-1]] = value

	def env_lookup(self, vname, env, depth=-1):
		if vname in env[1]:
			return (env[1])[vname]
		elif env[0] == None or depth==1:
			self.display('undefined variable ')# + vname)
			# exit(-1)
			return 'undefined'
			# raise NameError
		else:
			depth -= 1
			return self.env_lookup(vname, env[0])




	def test_envlookup(self):
		env = (None, {'a':3, 'er':'tes'})
		newenv = (env, {'a':6, 'r':34, 'rest':'ters'})
		newenv2 = (newenv, {'a':5, 'w':567, 'ew':'ksli'})
		print self.env_lookup('a', newenv)
		print self.env_lookup('er', newenv2)
		print self.env_lookup('ewer', newenv2)



if __name__ == '__main__':
	from Lexer import RheeLexer
	from Parser import RheeParser
	tokens = []
	from Lexer import tokens
	myLexer = RheeLexer()
	myLexer.build()
	myParser = RheeParser()
	myParser.build(myLexer)
	ast = myParser.test(u'''
क = ७
क = क + ७
क += ७
क लेख
	''', myLexer)

	# print ast

	myInterpreter = RheeInterpreter()
	myInterpreter.interpret(ast)

	# import json
	# print json.dumps(ast)

	# from TestSet import lextest

	# for i in lextest:
	# 	# print i
	# 	print i + "\t" +str(myInterpreter.num_mapper(lextest[i]))
	# myIntpreter.interpret(None, None)