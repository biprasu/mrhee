#encoding=utf8

from UnitInterpreter import UnitInterpreter

class RheeInterpreter(UnitInterpreter):
	"""docstring for RheeInterpreter"""

	environment = (None,{})

	# ibase = {'decimal': i_decimal,
	# 		'octal': i_octal,
	# 		'hexa': i_hexa,
	# 		'float': i_float,
	# 		'imaginary': i_imaginary,
	# 		'string': i_string,
	# 		'identifier': i_identifier,
	# 		'functioncall': i_functioncall,
	# 		'unaryminus': i_unaryminus,
	# 		'arithop': i_arithop,
	# 		'paranthesis': i_paranthesis,
	# 		'binop': i_binop,
	# 		'negation': i_negation,
	# 		'expression': i_expression,
	# 		'assign': i_assign,
	# 		'print': i_print,
	# 		'println': i_println,
	# 		'input': i_input,
	# 		'incremental': i_incremental,
	# 		'slif': i_slif,
	# 		'mlif': i_mlif,
	# 		'forloop': i_forloop,
	# 		'whileloop': i_whileloop,
	# 		'repeatloop': i_repeatloop,
	# 		'functiondef': i_functiondef,
	# 		'classdef': i_classdef,}

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
			elif stmt == 'identifier':
				return self.env_lookup(tree[2], env)
			elif stmt == 'functioncall':
				return self.i_functioncall(tree, env)
			elif stmt == 'reference':
				return self.i_reference(tree, env)
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
				self.add_to_env(env, tree[2], self.interpret(tree[3], env))
			elif stmt == 'print':
				self.i_print(tree[2], env)
			elif stmt == 'println':
				self.i_println(tree[2], env)
			elif stmt == 'input':
				self.i_input(tree[2], env)
			elif stmt == 'increment':
				self.i_increment(tree, env)
			elif stmt == 'return':  #?
				self.i_return(tree, env)
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
			else:
				self.display('unimplemented handle for ' + stmt)



	def add_to_env(self, env, vname, value):
		(env[1])[vname] = value
	def env_update(self, env, vname, value):	# @TODO get detail about the variable scope management
		(env[1])[vname] = value
		return True
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
	ast = myParser.test(u'''क = ४
	ख = ९
	काम टेस्ट(ख, ग)
		काम टेस्ट(ख, ग)
			७ चोटि
				क, ख, ग लेख
			टिचो
			७ * ७ पठाउ
		मका
		टेस्ट(९९९९९९, ९९९९) लेख
		७ पठाउ
	मका
	टेस्ट(९९, ९९९) लेख
		''', myLexer)

	myInterpreter = RheeInterpreter()
	myInterpreter.interpret(ast)

	import json
	print json.dumps(ast)

	# from TestSet import lextest

	# for i in lextest:
	# 	# print i
	# 	print i + "\t" +str(myInterpreter.num_mapper(lextest[i]))
	# myIntpreter.interpret(None, None)