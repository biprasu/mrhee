#encoding=UTF8
# def test(help):
# 	return help[0]

# mapper ={
# 	'tes' : lambda x: x[0]
# }

# print mapper['tes']([3,4])

# i = [4,5]

# for i[0] in xrange(6):
# 	pass
# print i[0] 

from Lexer import RheeLexer


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

# a = {'sd':3}
# print a.get('sd', "test")
# exit(0)

# Parser Zone
from Parser import RheeParser									# parser was an in-built library X.X
tokens = []
from Lexer import tokens

program = u'''
काम रचना()
			क = ५
			ग = ७
		मका
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

# program = u'''
# क = [३,४,५,[३,२,'test']]
# क लेख
# //क[क[३][१]*२/४] लेख
# //क[२] = ६७
# //क लेख
# '''#4

# program = u'''क = चित्र("ेख", ७०, ७०)
# क लुकाउ
# क देखाउ
# क बनाउ
# क मेटाउ
# क मा 'गोलो' कोर ७,७,७,४,'हरियो','हरियो'
# क मा 'कोठा' कोर ७,७,४४,४,४,'हरियो','हरियो'
# क मा 'लाइन' कोर ७,७,७,४४,४,'हरियो'
# क मा 'डट' कोर ७,७,७,'हरियो'
# क मा 'शब्द' कोर ७,७,"हरि", ७, 'हरियो'
# जब सम्म साचो छ
# 	ख = बटन()
# 	यदि ख == ३८ भए   //अप बटन
# 	   क मेटाउ
# 	   क मा 'डट' कोर १०,१०,३, "रातो"
# 	 अथवा ख == ४० भए  //डाउन बटन
# 	   क मेटाउ
# 	   क मा 'लाइन' कोर १०,१०,१००,१००, ३, "रातो"
# 	 अथवा ख == ३७ भए  //लेफ्ट बटन
# 	   क मेटाउ
# 	   क मा 'कोठा' कोर १०,१०,१००,१००, ३, "रातो", "निलो"
# 	 अथवा ख == ३९ भए  //राइट बटन
# 	   क मेटाउ
# 	   क मा 'गोलो 'कोर १००,१००,२०,    ३, "रातो", "निलो"
# 	  अथवा ख == ८३ भए // s बटन
# 	   बाहिर
# 	 दिय
# 	 क बनाउ
# बज	
# क हटाउ
# '''
# program = u'''
# क = ४
# क += ४
# क लेख
# '''

myLexer = RheeLexer()
myLexer.build()
# d evil 
# myLexer.test(program)

myParser = RheeParser()
myParser.build(myLexer)
ast = myParser.test(program, myLexer)
print ast
# interpreter zone
# from interpret import RheeInterpreter
# from UnitInterpreter import TracebackException


# try:
# 	myInterpreter = RheeInterpreter()
# 	myInterpreter.interpret(ast)
# except TracebackException as e:
# 	print e.message


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


# maps = {int:'test'}
# print maps[type(7)]
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

# def multi(test, teste):
# 	return (teste, test)

# test = 34
# teste = 3

# test,teste = multi(test, teste)
# print test, teste

# lhs,rhs = 2,3
# print lhs,rhs

# print u'क'>u'ख'

# import RheeTypeCheck
# def testTyrror():
# 	test = RheeTypeCheck()
# 	print(test.e_print("43"))
# 	print(test.e_print(43))
# 	print(test.e_print(43e-3))
# 	print(test.e_print(43e49))
# 	print(test.e_print(None))
# 	print(test.e_print(True))
# 	print(test.e_print(False))
# 	print(test.e_print(["43", 43, True, False, [None, 4e67, True]]))
# 	print(test.e_print(('function', 'fparams', 'fbody', 'fenv', 'fname')))
# 	print(test.e_print(('object', 'oenv', 'cname')))
# 	print(test.e_print(('class', 'cenv', 'cname')))

