#encoding=utf8

map_num = {u'\u0966':'0', u'\u0967':'1', u'\u0968':'2', u'\u0969':'3',
            u'\u096a':'4', u'\u096b':'5', u'\u096c':'6', u'\u096d':'7',
            u'\u096e':'8' ,u'\u096f':'9'
            }

def to_ascii(uni):
    temp = ''
    for digit in uni:
        temp += map_num[digit] if (digit in map_num) else digit
    return temp

def unicode_to_str(uni):
    temp = 'u'
    for digit in uni:   temp += str(hex(ord(digit)))
    return temp


class RheeCompiler:
    """docstring for RheeCompiler"""

    tab = ''
    env = (None, 'env')

    def __init__(self, targetfilename='temp.py'):
        self.temp = open(targetfilename,'wb')
        self.temp.write('#encoding=UTF8\n\n')

    def compile(self, trees, tab = None, fxn = None):
        if not tab: tab = self.tab

        for tree in trees:
            # print tree
            if not tree:	continue

            stmt = tree[0]
            if stmt == None:    continue
            lineno = tree[1]

            if stmt == 'decimal':
                return to_ascii(tree[2])
            elif stmt == 'octal':
                return to_ascii(tree[2])
            elif stmt == 'hexa':
                return to_ascii(tree[2])
            elif stmt == 'float':
                return to_ascii(tree[2])
            elif stmt == 'imaginary':
                return to_ascii(tree[2])+'j'

            elif stmt == 'string':
                return '\''+ tree[2] + '\''
                # return '\''+ tree[2].encode('utf8') +'\''
            elif stmt == 'null':
                return 'None'
            elif stmt == 'true':
                return 'True'
            elif stmt == 'false':
                return 'False'
            elif stmt == 'array':
                array_stmt = "["
                for t in tree[2]: array_stmt += self.compile(t) + ' ,'
                array_stmt += "]"
                return array_stmt

            elif stmt == 'identifier':
                return unicode_to_str(tree[2])

            elif stmt == 'functioncall':
                fname = unicode_to_str(tree[2])
                args = tree[3]

                stmt = fname + "("
                for arg in args:    stmt += self.compile(arg) + ","
                stmt += ")"
                return stmt

            elif stmt == 'aryreference':
<<<<<<< HEAD
                ident = self.compile([tree[2]])
                indices = tree[3]
                for item in indices:
                    start = self.compile(item[2])
                    if item[0] == 'normal':
                        return ident + "[" + str(start) +"]"
                    else:
                        end = self.compile(item[3])
                        return ident + "[" + str(start) + ":" + str(end) + "]"

            elif stmt == 'reference':
                item = tree[2][0]
=======
                ident = tree[2]
>>>>>>> 96b841c74020d61020857afba43235757948c6a2


            elif stmt == 'unaryminus':
                return '(-1*' + self.compile(tree[2]) +')'

            elif stmt == 'arithop':
                operator = tree[2]
                lhs = self.compile(tree[3])
                rhs = self.compile(tree[4])
                # + - * / % ^
                if operator == '^':
                    return lhs + ' ** ' + rhs
                else:
                    return lhs + operator + rhs


            elif stmt == 'paranthesis':
                return '('+self.compile(tree[2])+')'

            elif stmt == 'binop':
                operator = tree[2]
                lhs = self.compile(tree[3])
                rhs = self. compile(tree[4])
                # < > <= >= == !=
                if operator == u'वा':
                    return lhs + ' or ' + rhs
                elif operator == u'र':
                    return lhs + ' and ' + rhs
                else:
                    return lhs + operator + rhs

            elif stmt == 'negation':
                operator = tree[2]
                if operator == u'छ':
                    return self.compile(tree[3])
                elif operator == u'छैन':
                    return 'not(' + self.compile(tree[3]) +')'

            elif stmt == 'expression':
                self.temp.write(tab + self.compile(tree[2]).encode('utf8')+  "#"+str(lineno) +'\n')

            elif stmt == 'assign':
                refernc = tree[2]
                if refernc[0] == 'identifier':
<<<<<<< HEAD
                    assign_stat = unicode_to_str(refernc[2]) + ' = '+ self.compile(tree[3]).encode('utf8')+  "#"+str(lineno) + '\n'
=======
                    assign_stat = unicode_to_str(refernc[2]) + ' = '+ self.compile(tree[3]).encode('utf8') + '\n'
>>>>>>> 96b841c74020d61020857afba43235757948c6a2
                # elif refernc[0] == 'aryreference':

                # assign_stat = unicode_to_str(refernc[2]) + ' = '+ self.compile(tree[3]).encode('utf8') + '\n'
                self.temp.write(tab + assign_stat)

            elif stmt == 'print':
                print_stmt = ''
                for item in tree[2]:
                    print_stmt += 'print ' + self.compile(item)+  "#"+str(lineno) + '\n'
                self.temp.write(tab + print_stmt.encode('utf8'))

            elif stmt == 'println':
                print_stmt = 'print '
                for item in tree[2]:
                    print_stmt += self.compile(item) +', '
                print_stmt += '\'\'' +  "#"+str(lineno) +'\n'
                self.temp.write(tab + print_stmt.encode('utf8'))

            elif stmt == 'input':
                input_stmt = ''
                for item in tree[2]:
                    tag = item[0][0]
                    if tag == 'identifier':
                        var  = unicode_to_str(item[0][2])
                        input_stmt += var + ', '
<<<<<<< HEAD
                input_stmt = input_stmt[:-2]+ ' = raw_input()'+  "#"+str(lineno) +'\n'
=======
                input_stmt = input_stmt[:-1]+ ' = raw_input()\n'
>>>>>>> 96b841c74020d61020857afba43235757948c6a2
                self.temp.write(tab + input_stmt.encode('utf8'))

            elif stmt == 'increment':
                operator = tree[2]
                inc = self.compile(tree[4])
                iden = tree[3]
                inc_stmt = unicode_to_str(iden) + ' ' + operator + ' ' + inc +  "#"+str(lineno) + '\n'
                self.temp.write(tab + inc_stmt.encode('utf8'))

            elif stmt == 'return':
                return_stmt = 'return '
                for ele in tree[1]:
                    return_stmt += self.compile([ele]) + ','
                return_stmt = return_stmt[:-1] + "#"+str(lineno) +  '\n'
                self.temp.write(tab + return_stmt.encode('utf8'))

            elif stmt == 'continue':
                return 'continue'
            elif stmt == 'break':
                return 'break'

            elif stmt == 'slif':
                if_stmt = 'if ' + self.compile(tree[2]) + " :" + "#"+str(lineno) +"\n"
                self.temp.write(tab + if_stmt.encode('utf8'))
                self.compile(tree[3], tab+'\t')
                if tree[4]:
                    if_stmt = 'else: '+ "#"+str(lineno) +'\n'
                    self.temp.write(tab + if_stmt.encode('utf8'))
                    self.compile(tree[4], tab+'\t')

            elif stmt == 'mlif':
                if_stmt = 'if ' + self.compile(tree[2]) + " :"+ "#"+str(lineno) +"\n"
                self.temp.write(tab + if_stmt.encode('utf8'))
                self.compile(tree[3], tab+'\t')
                if tree[4]:
                    for elblock in tree[4]:
                        tag = elblock[0]
                        if tag == 'else-if':
                            if_stmt = 'elif ' + self.compile(elblock[2]) + " :"+ "#"+str(lineno)+"\n"
                            self.temp.write(tab + if_stmt.encode('utf8'))
                            self.compile(elblock[3], tab+'\t')
                        elif tag == 'else':
                            if_stmt = 'else: '+ "#"+str(lineno) +'\n'
                            self.temp.write(tab + if_stmt.encode('utf8'))
                            self.compile(elblock[2], tab+'\t')

            elif stmt == 'forloop':
                pre = self.compile(tree[3])
                post = self.compile(tree[4])
                inc = self.compile(tree[5])
                stmt_for = "for "+ unicode_to_str(tree[2]) + " in range(" + pre + "," + post + "," + inc +"):"+ "#"+str(lineno) +"\n"
                self.temp.write(tab + stmt_for.encode('utf8'))
                self.compile(tree[6], tab+'\t')

            elif stmt == 'whileloop':
                while_stmt = 'while ' + self.compile(tree[2]) + ':'+ "#"+str(lineno)+'\n'
                self.temp.write(tab + while_stmt.encode('utf8'))
                self.compile(tree[3],tab+'\t')

            elif stmt == 'repeatloop':
                iter = self.compile(tree[2])
                repeat_stmt = 'for i in range(' + iter + '):'+ "#"+str(lineno) +'\n'
                self.temp.write(tab + repeat_stmt.encode('utf8'))
                self.compile(tree[3],tab+'\t')

            elif stmt == 'functiondef':
                fname = tree[2]
                fname_str = unicode_to_str(fname)
                fparams = tree[3]
                fbody = tree[4]
                if fxn == 'class':
                    function_stmt = "def " + (fname_str if fname != u'रचना' else '__init__') + "(self,"
                else:   function_stmt = "def " + fname_str + "("
                for param in fparams:   function_stmt += unicode_to_str(param) +", "
                function_stmt += ") :"+ "#"+str(lineno)+"\n"
                self.temp.write(tab + function_stmt)
                self.compile(fbody, tab+'\t')
                self.temp.write('\n')

            elif stmt == 'classdef':
                cname = unicode_to_str(tree[2])
                cbody = tree[3]
                class_stmt = "class " + cname +":"+ "#"+str(lineno)+"\n"
                self.temp.write(tab+class_stmt)
                self.compile(cbody,tab+'\t',fxn = 'class')
                self.temp.write('\n')


    def __del__(self):
        self.temp.write('\n\n')#import temp')
        self.temp.close()


from Lexer import RheeLexer
from Parser import RheeParser

def compile_file(filename, targetfilename="temp.py"):
    myLexer = RheeLexer()
    myLexer.build()
    myParser = RheeParser()
    myParser.build(myLexer)

    ast = myParser.test(open(filename,'r').read().decode('utf8'), myLexer)

    myCompiler = RheeCompiler(targetfilename)
    myCompiler.compile(ast)

if __name__ == '__main__':

    myLexer = RheeLexer()
    myLexer.build()
    myParser = RheeParser()
    myParser.build(myLexer)

    ast = myParser.test(u'''
<<<<<<< HEAD
	//क.क[४:४४] लेख
	क = ४
ख = ९
जब सम्म शुन्य छ वा झुटो छ
	क लेख
	क += १
बज
=======
	क[४] लेख
>>>>>>> 96b841c74020d61020857afba43235757948c6a2
                                ''', myLexer)

    myCompiler = RheeCompiler()
    myCompiler.compile(ast)