#encoding=UTF8

from Lexer import RheeLexer

myLexer = RheeLexer()
myLexer.build()
# for item in testset:
# 	myLexer.test(testset[item])
# 	print item

# myLexer.test(u'''यदि क==ख भए
# 	दिय''')
# from TestSet import gTest
# myParser = RheeParser()
# myParser.build(myLexer)
# myParser.test(gTest['normal'], myLexer)

# print int('0x34')
# print float('3.4e-3')

# exit(0)

# Parser Zone
from Parser import RheeParser									# parser was an in-built library X.X
tokens = []
from Lexer import tokens

program = u'''
	क = ४
	खाका वस्तु
		क = ४
		ख = ९
		काम रचना()
			क = ५
			ग = ७
		मका
		काम टेस्ट(क, ख, ग)
		७*८ चोटि
			क लेख
		टिचो
		मका
	काखा
	त = वस्तु()
	त लेख
	'''

myLexer.test(program)
myParser = RheeParser()
myParser.build(myLexer)
ast = myParser.test(program, myLexer)

# interpreter zone
from interpret import RheeInterpreter

myInterpreter = RheeInterpreter()
myInterpreter.interpret(ast)
# print myInterpreter.environment

# print len([])


# def f():
# 	a = []
# 	return a

# print len(f())
# a = raw_input("test")

# check for locality of reference
# if True:
# 	b3=9
# 	print b3
# print b3



# print 4%3
# print 4^4
# print pow(4,2)
# print ('\n\n'),
# print int('0767', 8)
# for testing the num_mapper
# myInterpreter = RheeInterpreter()

# from TestSet import lextest

# for i in lextest:
# 	# print i
# 	print i + "\t" +str(myInterpreter.num_mapper(lextest[i]))
		