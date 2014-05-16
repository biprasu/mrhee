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
				pass
			elif stmt == 'hexa':
				pass
			elif stmt == 'float':
				return self.num_mapper(tree[2])
			elif stmt == 'imaginary':
				pass
			elif stmt == 'string':
				return tree[2]
			elif stmt == 'identifier':
				return self.env_lookup(tree[2], env)
			elif stmt == 'functioncall':
				pass
			elif stmt == 'unaryminus':
				return -1 * self.interpret(tree[2], env)
			elif stmt == 'arithop':
				return self.i_arithop(tree, env)
			elif stmt == 'paranthesis':
				return self.interpret(tree[2], env)
			elif stmt == 'binop':
				return self.i_binop(tree, env)
			elif stmt == 'negation':
				pass
			elif stmt == 'expression':
				pass
			elif stmt == 'assign':
				pass
			elif stmt == 'print':
				self.i_print(tree, env)
			elif stmt == 'println':
				self.i_print(tree[2], env)
			elif stmt == 'input':
				pass
			elif stmt == 'incremental':
				pass
			elif stmt == 'slif':
				pass
			elif stmt == 'mlif':
				pass
			elif stmt == 'forloop':
				pass
			elif stmt == 'whileloop':
				pass
			elif stmt == 'repeatloop':
				pass
			elif stmt == 'functiondef':
				pass
			elif stmt == 'classdef':
				pass





if __name__ == '__main__':
	from Lexer import RheeLexer
	from Parser import RheeParser
	tokens = []
	from Lexer import tokens
	myLexer = RheeLexer()
	myLexer.build()
	myParser = RheeParser()
	myParser.build(myLexer)
	ast = myParser.test(u'''-(९^३)*९/४ लेख
		''', myLexer)

	myInterpreter = RheeInterpreter()
	myInterpreter.interpret(ast)

	# from TestSet import lextest

	# for i in lextest:
	# 	# print i
	# 	print i + "\t" +str(myInterpreter.num_mapper(lextest[i]))
	# myIntpreter.interpret(None, None)