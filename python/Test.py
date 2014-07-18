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
		काम फ़क्तोरिअल् (ल)
			यदि ल==१ भए १ पठाउ अथवा ल * फ़क्तोरिअल्(ल-१) पठाउ
		मका
	काखा
	त = वस्तु()
	त.फ़क्तोरिअल्(५) लेख
	त.क = ७० 
	त.क लेख
	प् = [३,४,५]
	प्[२] = ९०
	प् लेख
	'''

program = u'''
क = [३,४,५,[३,२,'test']]
क[क[३][१]*२/४] लेख
क[२] = ६७
क लेख
'''#4

program = u'''
क = ३
सबै ख = १ देखि ९ 
	क += १
	यदि क==५ भए
		अर्को
	अथवा क ==७ भए
		बाहिर
	दिय
	क लेख
	
बैस
'''

myLexer.test(program)
myParser = RheeParser()
myParser.build(myLexer)
ast = myParser.test(program, myLexer)

# interpreter zone
from interpret import RheeInterpreter

myInterpreter = RheeInterpreter()
myInterpreter.interpret(ast)

# print type(4) is tuple
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
# @TODO infinite recursion problem