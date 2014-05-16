#encoding=UTF8

from Lexer import RheeLexer
# from TestSet import testset
from Parser import RheeParser									# parser was an in-built library X.X

myLexer = RheeLexer()
myLexer.build()
# for item in testset:
# 	myLexer.test(testset[item])
# 	print item

myLexer.test(u'''यदि क==ख भए
	दिय''')
# from TestSet import gTest
# myParser = RheeParser()
# myParser.build(myLexer)
# myParser.test(gTest['normal'], myLexer)

# print int('0x34')
print float('3.4e-3')

# exit(0)

class test(object):
	"""docstring for test"""
	a = 4
	if a:
		print a
		
	def __init__(self, arg):
		super(test, self).__init__()
		self.arg = arg


print 4%3
print 4^4
print pow(4,2)
# for testing the num_mapper
# myInterpreter = RheeInterpreter()

# from TestSet import lextest

# for i in lextest:
# 	# print i
# 	print i + "\t" +str(myInterpreter.num_mapper(lextest[i]))
		