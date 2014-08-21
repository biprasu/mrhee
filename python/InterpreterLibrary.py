#encoding=UTF8

import os
import codecs
from Tkinter import *
# import NepInterpreter as NI


class ArgumentError(Exception):
    pass

# class BreakError(Exception):
#     pass
# class ReturnError(Exception):
#     pass

# class ContinueError(Exception):
#     pass


# class NotANumber(Exception):
#     pass


to_col = {

    u"रातो" : "red",
    u"हरियो" : "green",
    u"निलो" : "blue",
    u"खैरो" : "brown",
    u"सुन्तला" : "orange",
    u"कालो" : "black",
    u"सेतो" : "white",
    u"पहेलो" : "yellow",
    u"प्याजि" : "purple",
    u"रानि" : "pink",
}








# def count(args, env):
#     # if (!args) raise ArgumentError
#     if (len(args) != 1):
#         raise ArgumentError
#     return NI.to_unicode(len(NI.interpret(args[0],env)))

# def breakString(args, env):
#     if (len(args) != 2):
#         raise ArgumentError

#     string = NI.interpret(args[0], env)
#     pattern = NI.interpret(args[1], env)

#     # type checking we accept only unicode string
#     if type(string) != type(u'ल') or type(u'ल') != type(pattern):
#         raise ArgumentError

#     return string.split(pattern)

# def findString(args, env):
#     if (len(args) < 2 or len(args) > 4):
#         raise ArgumentError
#     string = NI.interpret(args[0], env)
#     pattern = NI.interpret(args[1], env)
#     begin = (len(args)>2) and NI.interpret(args[2], env) or u'०'
#     end =   (len(args)>3) and NI.interpret(args[3], env) or u'०'

#     if type(string) != type(u'ल') \
#        or type(u'ल') != type(pattern) \
#        or type(u'ल') != type(pattern) \
#         or type(u'ल') != type(pattern):
#         raise ArgumentError

#     begin = int(NI.to_ascii(begin))
#     end = int(NI.to_ascii(end))
    
#     if (end != 0):
#         return NI.get_key_from_value(NI.map_num, string.find(pattern, begin, end))
#     return NI.to_unicode(string.find(pattern, begin))

# def replaceString(args, env):
#     if len(args) != 3:
#         raise ArgumentError
#     s = NI.interpret(args[0], env)
#     os = NI.interpret(args[1], env)
#     ns = NI.interpret(args[2], env)
#     if type(s) != type(u'ल') \
#         or type(u'ल') != type(os)\
#         or type(ns) != type(u'ल'):
#         raise ArgumentError
#     return s.replace(os, ns)

# def isNumber(args,env):
#     if len(args) != 1:
#         raise ArgumentError
#     for item in NI.interpret(args[0], env):
#         if ((not item in NI.map_num) and item != u'.' and item != u'-'):
#             return u'०'
#     return u'१'

# def toNumber(args,env):
#     if len(args) != 1:
#         raise ArgumentError
#     for item in NI.interpret(args[0], env):
#         if ((not item in NI.map_num) and item != u'.' and item != u'-'):
#             raise NotANumber
#     return (NI.interpret(args[0], env))

# def trimString(args,env):
#     if len(args) != 1:
#         raise ArgumentError
#     return NI.interpret(args[0]).strip(" ")

# import math
# import random
# def squareRoot(args, env):
#     if len(args) != 1:
#         raise ArgumentError
#     return NI.to_unicode(math.sqrt(NI.to_ascii(NI.interpret(args[0], env))))

# def randomNumber(args, env):
#     return NI.to_unicode(int(random.random()*1000))

# def joinString(args, env):
#     return ''.join([NI.interpret(args[0], env), NI.interpret(args[1], env)])
class InterpreterLibs:
    def openfile(self,args):
        if len(args)!= 2:   raise ArgumentError()

        filename = args[0]
        mode = args[1]

        if mode == u'लेख्न':
            return ("fileobject", "w", codecs.open(filename,"w",encoding="UTF8"))
        elif mode == u'पढ्न':
            if not os.path.exists(filename):
                raise IOError
                #return a generator, then we'll just do writes

            #return the file, but also save the generator so as to use it later
            file = codecs.open(filename,"r",encoding="UTF8")
            # filename += u"generator"
            gen = (i for i in file.readlines())
            return ("fileobject",'r',file,gen)

        elif mode == u'जोड्न':
            return ("fileobject", 'a', codecs.open(filename,"a",encoding="UTF8"))
        else:
            self.error ("illegal mode for file access")

    def readfile(self, args):
        fileref = args[0]

        if fileref[0] != 'fileobject':
            self.error("Cannot perform file operation non file object")
        if fileref[1] != 'r':
            self.error("File Should be opened in read mode")
        
        filegen = fileref[3]
        try:
            a = filegen.next()
            return a[:-1]
        except StopIteration:
            return None


    def writefile(self,args):
        fileref = args[0]

        if fileref[0] != 'fileobject':
            self.error("Cannot perform file operation non file object")
        if fileref[1] != 'w' and fileref[1] != 'a':
            self.error("File Should be opened in write or append mode")

        for items in args[1:]:
            fileref[2].write(items)
        return

    def writefileln(self, args):
        fileref = args[0]

        if fileref[0] != 'fileobject':
            self.error("Cannot perform file operation non file object")
        if fileref[1] != 'w' and fileref[1] != 'a':
            self.error("File Should be opened in write or append mode")

        for items in args[1:]:
            fileref[2].write(items)
        fileref[2].write("\n")
        return

    def closefile(self, args):
        fileref = args[0]

        if fileref[0] != 'fileobject':
            self.error("Cannot perform file operation non file object")
        
        file = fileref[2]
        file.close()

    keyboard_keys = []

    def keyboardhandler(self, event):
        self.keyboard_keys.append(event.keycode)
        return


    def keyboardgetkeys(self, args):
        if args:
            raise ArgumentError()
        
        if self.keyboard_keys:
            return self.keyboard_keys.pop(0)
        else:
            return 0

    def initgraphics(self, args):
        root = Tk()
        if len(args) < 3:
            raise ArgumentError()

        name = args[0]
        name = name.encode('UTF8')
        height = int(args[1])
        width = int(args[2])

        root.title(name)
        root.configure(height=height, width=width)  #set width and height
        root.resizable(0,0)                         #disable resizing
        canvas = Canvas(root,width=width,height=height)
        canvas.pack(fill='both')

        #hide the windows
        root.withdraw()
        root.bind("<Key>",self.keyboardhandler)
        return ("graphicobject",root,canvas)


    def hidegraphics(self, args):
        if len(args) != 1:
            raise ArgumentError()
        root = args[0][1]
        root.withdraw()
        return

    def showgraphics(self, args):
        if len(args) != 1:
            raise ArgumentError()
        root = args[0][1]
        root.deiconify()
        root.update()
        return

    def cleargraphics(self, args):
        if len(args) != 1:
            raise ArgumentError()
        root,canvas = args[0][1],args[0][2]
        canvas.delete(ALL)
        root.update()
        return

    def closegraphics(self, args):
        if len(args) != 1:
            raise ArgumentError()
        root = args[0][1]
        root.destroy()
        return

    def updategraphics(self, args):
        if len(args) != 1:
            raise ArgumentError()

        root = args[0][1]
        try:
            root.update()
        except:
            pass
        return


    def drawgraphics(self, args):
        
        if args[1] == u"गोलो":
             self.drawcircle(args)
        elif args[1] == u"कोठा":
             self.drawrectangle(args)
        elif args[1] == u"लाइन":
             self.drawline(args)
        elif args[1] == u"डट":
             self.drawpoint(args)
        elif args[1] == u"शब्द":
            self.drawtext(args)
        else:
            self.error("invalid argument to draw ")

        return


    def drawpoint(self, args):
        if len(args)<4 or len(args) > 6:
             raise ArgumentError()
        argnum = len(args)
        c1 = int(args[2])
        c2 = int(args[3])
        width = int(args[4]) if argnum>4 else None
        outline = to_col[args[5]] if argnum>5 else None
        
        root,canvas = args[0][1], args[0][2]
        canvas.create_rectangle(c1,c2,c1,c2,width=width,outline=outline)
        root.update()
        return

    def drawtext(self, args):
        if len(args)<5 or len(args) > 7:
             raise ArgumentError()
        argnum = len(args)
        c1 = int(args[2])
        c2 = int(args[3])
        text = args[4].encode("UTF8")
        size = int(args[5]) if argnum>5 else None
        color = to_col[args[6]] if argnum>6 else None
        font = "a " + str(size) if size is not None else "0 "
        
        root,canvas = args[0][1], args[0][2]
        canvas.create_text(c1,c2,text=text,font=font,fill=color,anchor="nw")
        root.update()
        return

    def drawline(self, args):
        'requires the canvas, 4 coords compulsory and width and foreground color optional'
        if len(args) < 6 or len(args) > 8:
             raise ArgumentError()
        argnum = len(args)
        
        c1 = int(args[2])
        c2 = int(args[3])
        c3 = int(args[4])
        c4 = int(args[5])
        width = int(args[6]) if argnum > 6 else None
        fill = to_col[args[7]] if argnum>7 else None
        
        root,canvas = args[0][1], args[0][2]
        canvas.create_line(c1,c2,c3,c4,width=width,fill=fill)
        canvas.update()
        return



    def drawcircle(self, args):
        'requres canvas, 2 coords, radius compulsory; width, outline, fill optional'
        if len(args) < 5 or len(args) > 8:
             raise ArgumentError()
        argnum = len(args)
        
        x = int(args[2])
        y = int(args[3])
        r = int(args[4])
        width = int(args[5]) if argnum>5 else None
        outline = to_col[args[6]] if argnum>6 else None
        fill = to_col[args[7]] if argnum>7 else None
        
        root,canvas = args[0][1], args[0][2]
        canvas.create_oval(x-r,y-r,x+r,y+r,width=width,fill=fill,outline=outline)
        canvas.update()
        return

    def drawrectangle(self, args):
        'requires the canvas, 4 coords compulsory and width and foreground color optional'
        if len(args) < 6 or len(args) > 9:
             raise ArgumentError()
        argnum = len(args)

        c1 = int(args[2])
        c2 = int(args[3])
        c3 = int(args[4])
        c4 = int(args[5])
        width = int(args[6]) if argnum>6 else None
        outline = to_col[args[7]] if argnum>7 else None
        fill = to_col[args[8]] if argnum>8 else None
        
        root,canvas = args[0][1], args[0][2]
        canvas.create_rectangle(c1,c2,c3,c4,width=width,fill=fill,outline=outline)
        canvas.update()
        return

    function_names = {
        u'फाइलखोल' : openfile,
        u'__बन्दगर__' : closefile,
        u"__फाइलपढ__" : readfile,
        u"__फाइललेख__" : writefile,
        u"__फाइललेखलाइन__" : writefileln,

        u"चित्र" : initgraphics,
        u"__देखाउ__" : showgraphics,
        u"__लुकाउ__" : hidegraphics,
        u"__बनाउ__" : updategraphics,
        u"__मेटाउ__" : cleargraphics,
        u"__कोर__" : drawgraphics,
        u"__हटाउ__" : closegraphics,
        u"बटन" : keyboardgetkeys,
        
        # u'गन' : count,
        # u'टुक्राऊ' : breakString,
        # u'खोज'     : findString,
        # u'बद्ल'     : replaceString,
        # u'अ‍कंहो'  : isNumber,
        # u'अ‍कं'     : toNumber,
        # u'खालीहताऊ' : trimString,
        # u'वर्गरुट' : squareRoot,
        # u'अनियमित' : randomNumber,
    }


    def checklibrary(self, fname):
        if fname not in self.function_names:
            return False
        return True

    def call(self, fname, args, env):
        iargs = [self.interpret(a, env) for a in args]
        return self.function_names[fname](self, iargs)
