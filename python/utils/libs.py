#encoding=UTF8

import os
import codecs
from Tkinter import *
import random

to_col = {

    "रातो" : "red",
    "हरियो" : "green",
    "निलो" : "blue",
    "खैरो" : "brown",
    "सुन्तला" : "orange",
    "कालो" : "black",
    "सेतो" : "white",
    "पहेलो" : "yellow",
    "प्याजि" : "purple",
    "रानि" : "pink",
}

def randomnum():
    return random.randint(0, 1000000)

def openfile(args):
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

def readfile(args):
    fileref = args[0]

    filegen = fileref[3]
    try:
        a = filegen.next()
        return a[:-1]
    except StopIteration:
        return None


def writefile(args):
    fileref = args[0]

    for items in args[1:]:
        fileref[2].write(items)
    return

def writefileln(args):
    fileref = args[0]

    for items in args[1:]:
        fileref[2].write(items)
    fileref[2].write("\n")
    return

def closefile(args):
    fileref = args[0]

    file = fileref[2]
    file.close()

keyboard_keys = []

def keyboardhandler(event):
    keyboard_keys.append(event.keycode)
    return


def keyboardgetkeys():
    
    if keyboard_keys:
        return keyboard_keys.pop(0)
    else:
        return 0

root = None
canvas = None
def initgraphics(args):
    global root, canvas
    root = Tk()

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
    root.bind("<Key>",keyboardhandler)
    return ("graphicobject",root,canvas)


def hidegraphics(args):
    global root, canvas
    root = args[0][1]
    root.withdraw()
    return

def showgraphics(args):
    global root, canvas
    root = args[0][1]
    root.deiconify()
    root.update()
    return

def cleargraphics(args):
    global root, canvas
    root,canvas = args[0][1],args[0][2]
    canvas.delete(ALL)
    root.update()
    return

def closegraphics(args):
    global root, canvas
    root = args[0][1]
    root.destroy()
    return

def updategraphics(args):
    global root, canvas

    root = args[0][1]
    try:
        root.update()
    except:
        pass
    return


def drawgraphics(args):
    
    if args[1] == "गोलो":
         drawcircle(args)
    elif args[1] == "कोठा":
         drawrectangle(args)
    elif args[1] == "लाइन":
         drawline(args)
    elif args[1] == "डट":
         drawpoint(args)
    elif args[1] == "शब्द":
        drawtext(args)

    return


def drawpoint(args):
    global root, canvas
    argnum = len(args)
    c1 = int(args[2])
    c2 = int(args[3])
    width = int(args[4]) if argnum>4 else None
    outline = to_col[args[5]] if argnum>5 else None
    
    root,canvas = args[0][1], args[0][2]
    canvas.create_rectangle(c1,c2,c1,c2,width=width,outline=outline)
    root.update()
    return

def drawtext(args):
    global root, canvas
    argnum = len(args)
    c1 = int(args[2])
    c2 = int(args[3])
    text = args[4]
    size = int(args[5]) if argnum>5 else None
    color = to_col[args[6]] if argnum>6 else None
    font = "a " + str(size) if size is not None else "0 "
    
    root,canvas = args[0][1], args[0][2]
    canvas.create_text(c1,c2,text=text,font=font,fill=color,anchor="nw")
    root.update()
    return

def drawline(args):
    'requires the canvas, 4 coords compulsory and width and foreground color optional'

    global root, canvas

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



def drawcircle(args):
    'requres canvas, 2 coords, radius compulsory; width, outline, fill optional'
    global root, canvas
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

def drawrectangle(args):
    'requires the canvas, 4 coords compulsory and width and foreground color optional'
    global root, canvas
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

# def draw(args):
#     master, canvas = args[0]
#     draw_type = args[1]


def checklibrary(fname):
    if fname not in function_names:
        return False
    return True

def call(fname, args, env):
    iargs = [interpret(a, env) for a in args]
    return function_names[fname](iargs)
