#encoding=utf8

import os
import shutil

map_num = {u'\u0966':'0', u'\u0967':'1', u'\u0968':'2', u'\u0969':'3',
            u'\u096a':'4', u'\u096b':'5', u'\u096c':'6', u'\u096d':'7',
            u'\u096e':'8' ,u'\u096f':'9'
            }

choti_loop = 0
def get_underscore():
    underscore = '_'
    return underscore*choti_loop

def to_ascii(uni):
    temp = ''
    for digit in uni:
        temp += map_num[digit] if (digit in map_num) else digit
    return temp

def unicode_to_str(uni):
    temp = 'u'
    temp += uni.encode('utf-8').encode('hex')
    return temp

class TracebackException(Exception):
	def __init__(self, message):
		Exception.__init__(self, message)

class RheeCompiler:
    """docstring for RheeCompiler"""

    tab = ''
    env = (None, 'env')

    def __init__(self, targetfilename='temp.py'):
        self.temp = open(targetfilename,'wb')

        filepath = os.path.abspath(targetfilename)
        directory = os.path.split(filepath)[0]
        shutil.copy2('libs.py', directory)

        self.temp.write('#encoding=UTF8\nimport codecs\nfrom Tkinter import *\n')
        self.temp.write('from libs import *\n\n')

    def compile(self, trees, tab = None, fxn = None):
        if not tab: tab = self.tab

        for tree in trees:
            # print tree
            if not tree:	continue
            # print tree, '\n'
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
                args = tree[3]
                if tree[2] == u'अंक':
                    fname = 'float'
                    stmt = fname + "("
                    for arg in args:
                        if arg[0][0] == 'string':
                            stmt += "'" + str(to_ascii(arg[0][2])) + "'" + ","
                        else:   stmt += self.compile(arg) + ","
                    stmt += ")"

                elif tree[2] == u'शब्द':
                    fname = 'str'
                    stmt = fname + "("
                    for arg in args:
                        if arg[0][0] == 'decimal':
                            stmt += "'" + arg[0][2] + "'" + ","
                        else:   stmt += self.compile(arg) + ","
                    stmt += ")"

                elif tree[2] == u'फाइलखोल':
                    file_stmt = ''
                    # print tree[2]
                    filename = args[0][0][2]
                    # print filename
                    option = args[1][0][2]
                    # print option
                    option = "wb" if option ==  u"लेख्न"else ("rb" if option == u"पढ्न" else "ab")
                    return "open(u'" + filename + "','" + option + "')"

                elif tree[2] == u'__फाइललेखलाइन__' or tree[2] == u'__फाइललेख__':
                    fp = self.compile(args[0])
                    txt = ''
                    for arg in args[1:]:
                        txt += arg[0][2]
                    return fp + ".write('" + txt + ('\\n' if tree[2] == u'__फाइललेखलाइन__' else '') + "')"

                elif tree[2] == u'__बन्दगर__':
                    fp = self.compile(tree[3][0])
                    return fp + ".close()"

                elif tree[2] == u'__फाइलपढ__':
                    fp = self.compile(tree[3][0])
                    return fp + ".readline()"

                elif tree[2] == u'चित्र':
                    window_name = tree[3][0][0][2]
                    width, height = self.compile(tree[3][1]), self.compile(tree[3][2])
                    window_stmt = "initgraphics([u'"+ window_name + "',"+ str(height) +','+ str(width) +"])"
                    return window_stmt

                elif tree[2] == u'__देखाउ__':
                    wp = self.compile(tree[3][0])
                    return "showgraphics([[''," + wp + "]])"

                elif tree[2] == u'__बनाउ__':
                    wp = self.compile(tree[3][0])
                    return "updategraphics([[''," + wp + "]])"

                elif tree[2] == u'बटन':
                    return "keyboardgetkeys()"

                elif tree[2] == u'__कोर__':
                    wp = self.compile(tree[3][0])
                    # type = tree[3][]
                    return

                else:
                    fname = unicode_to_str(tree[2])
                    stmt = fname + "("
                    for arg in args:    stmt += self.compile(arg) + ","
                    stmt += ")"
                return stmt

            elif stmt == 'aryreference':
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
                # print tree
                ref_stmt = ''
                item = tree[2][0]

                retobj = self.compile([item])

                ref_stmt += retobj

                for item in tree[2][1:]:
                    ref_stmt += "." + self.compile([item])

                return ref_stmt

            elif stmt == 'meroref':
                return 'self.' + self.compile([tree[2]])


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
                    assign_stat = unicode_to_str(refernc[2]) + ' = '+ self.compile(tree[3]).encode('utf8')+  "#"+str(lineno) + '\n'
                elif refernc[0] == 'reference' or refernc[0] == 'aryreference':
                    assign_stat = self.compile([refernc]) + ' = ' + self.compile(tree[3]).encode('utf8')+  "#"+str(lineno) + '\n'


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
                input_stmt = input_stmt[:-2]+ ' = raw_input()'+  "#"+str(lineno) +'\n'
                self.temp.write(tab + input_stmt.encode('utf8'))

            elif stmt == 'increment':
                operator = tree[2]
                inc = self.compile(tree[4])
                iden = tree[3]
                inc_stmt = unicode_to_str(iden) + ' ' + operator + ' ' + inc +  "#"+str(lineno) + '\n'
                self.temp.write(tab + inc_stmt.encode('utf8'))

            elif stmt == 'return':
                return_stmt = 'return '
                for ele in tree[2]:
                    return_stmt += self.compile([ele]) + ','
                return_stmt = return_stmt[:-1] + "#"+str(lineno) +  '\n'
                self.temp.write(tab + return_stmt.encode('utf8'))

            elif stmt == 'continue':
                self.temp.write(tab + 'continue\n')
            elif stmt == 'break':
                self.temp.write(tab + 'break\n')

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
                global choti_loop
                choti_loop += 1
                iter = self.compile(tree[2])
                repeat_stmt = 'for ' + get_underscore() + ' in range(' + iter + '):'+ "#"+str(lineno) +'\n'
                self.temp.write(tab + repeat_stmt.encode('utf8'))
                self.compile(tree[3],tab+'\t')
                choti_loop -= 1

            elif stmt == 'functiondef':
                fname = tree[2]
                if fname == u'अंक':     fname_str = 'float'
                elif fname == u'शब्द':  fname_str = 'str'
                else:                   fname_str = unicode_to_str(fname)
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

    def error(self, msg, lineno=None, tb=None):
        if not tb:
            print "ERROR!! " + msg + " in line number "+ str(lineno);
        print "SamasyaSuchak: " + str(lineno)
        raise TracebackException("Trace it Back")
        exit(0)

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

    print myParser.syntaxErrors

    ast = myParser.test(open(filename,'r').read().decode('utf8'), myLexer)

    myCompiler = RheeCompiler(targetfilename)
    myCompiler.compile(ast)

if __name__ == '__main__':

    myLexer = RheeLexer()
    myLexer.build()
    myParser = RheeParser()
    myParser.build(myLexer)

    ast = myParser.test(u'''

क मा 'शब्द' कोर ७,७,"हरि", ७, 'हरियो'


    ''', myLexer)

    myCompiler = RheeCompiler()
    myCompiler.compile(ast)