#encoding=UTF8
import codecs
from Tkinter import *
from libs import *

ue0a495 = initgraphics([u'मेरो चित्र',1000,500])#1
showgraphics([ue0a495])#2
updategraphics([ue0a495])#3
ue0a49ae0a4b2e0a4bee0a489 = 1#5
ue0a496e0a4bee0a4a8e0a4be = []#6
ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be = []#7
ue0a4a6e0a4bfe0a4b6e0a4be = 'दायाँ'#8
def ue0a4b8e0a581e0a4a4() :#10
	for _ in range(3000):pass#11

def ue0a496e0a4bee0a4a8e0a4bee0a4ace0a4a8e0a4bee0a489() :#15
	ue0a496e0a4bee0a4a8e0a4be = [randomnum()%100 ,randomnum()%50 ,]#16
	return ue0a496e0a4bee0a4a8e0a4be#17

ue0a485 = 0#20
def ue0a4b8e0a4ace0a588e0a49ae0a4bfe0a4a4e0a58de0a4b0e0a495e0a58be0a4b0() :#22
	cleargraphics([ue0a495])#23
	drawgraphics([ue0a495,'कोठा',ue0a496e0a4bee0a4a8e0a4be[0]*10,ue0a496e0a4bee0a4a8e0a4be[1]*10,ue0a496e0a4bee0a4a8e0a4be[0]*10+10,ue0a496e0a4bee0a4a8e0a4be[1]*10+10,1,'निलो','हरियो'])#24
	for ue0a485 in range(0,len(ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be)/2,1):#25
		drawgraphics([ue0a495,'कोठा',((ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[(ue0a485*2)])*10),((ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[(ue0a485*2+1)])*10),((ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[(ue0a485*2)])*10+10),((ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[(ue0a485*2+1)]*10)+10),1,'निलो','निलो'])#26
	updategraphics([ue0a495])#28

def ue0a4b8e0a4ace0a588e0a4aee0a4bfe0a4b2e0a4bee0a489() :#31
	ue0a496e0a4bee0a4a8e0a4be = ue0a496e0a4bee0a4a8e0a4bee0a4ace0a4a8e0a4bee0a489()#32
	ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be = [20 ,10 ,21 ,10 ,]#33
	ue0a4a6e0a4bfe0a4b6e0a4be = 'दायाँ'#34

def ue0a487e0a4a8e0a58de0a4aae0a581e0a49fe0a495e0a587e0a49be0a4b9e0a587e0a4b0() :#38
	ue0a487e0a4a8e0a58de0a4aae0a581e0a49f = keyboardgetkeys()#39
	if ue0a487e0a4a8e0a58de0a4aae0a581e0a49f==27 :#40
		print 'इस्केप', ''#41
		ue0a49ae0a4b2e0a4bee0a489 = 0#42
	elif ue0a487e0a4a8e0a58de0a4aae0a581e0a49f==38 :#40
		ue0a4a6e0a4bfe0a4b6e0a4be = 'माथि'#44
		print ue0a4a6e0a4bfe0a4b6e0a4be, ''#45
	elif ue0a487e0a4a8e0a58de0a4aae0a581e0a49f==39 :#40
		ue0a4a6e0a4bfe0a4b6e0a4be = 'दायाँ'#47
	elif ue0a487e0a4a8e0a58de0a4aae0a581e0a49f==40 :#40
		ue0a4a6e0a4bfe0a4b6e0a4be = 'बाँया'#49
	elif ue0a487e0a4a8e0a58de0a4aae0a581e0a49f==37 :#40
		ue0a4a6e0a4bfe0a4b6e0a4be = 'तल'#51

ue0a49fe0a4bee0a489e0a495e0a58b = []#55
def ue0a4b8e0a4b0e0a58de0a4aae0a4b2e0a4bee0a488e0a4aee0a4bfe0a4b2e0a4bee0a489() :#56
	ue0a49fe0a4bee0a489e0a495e0a58b = ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[0:2]#57
	if ue0a4a6e0a4bfe0a4b6e0a4be=='दायाँ' :#58
		ue0a49fe0a4bee0a489e0a495e0a58b[0] = ue0a49fe0a4bee0a489e0a495e0a58b[0]+1#59
	elif ue0a4a6e0a4bfe0a4b6e0a4be=='बायाँ' :#58
		ue0a49fe0a4bee0a489e0a495e0a58b[0] = ue0a49fe0a4bee0a489e0a495e0a58b[0]-1#61
	elif ue0a4a6e0a4bfe0a4b6e0a4be=='तल' :#58
		ue0a49fe0a4bee0a489e0a495e0a58b[1] = ue0a49fe0a4bee0a489e0a495e0a58b[1]+1#63
	elif ue0a4a6e0a4bfe0a4b6e0a4be=='माथि' :#58
		ue0a49fe0a4bee0a489e0a495e0a58b[1] = ue0a49fe0a4bee0a489e0a495e0a58b[1]-1#65
	ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be = ue0a49fe0a4bee0a489e0a495e0a58b+ue0a4b8e0a4b0e0a58de0a4aae0a495e0a58be0a4a1e0a4bee0a4a4e0a4be[0:2]#67
	if ue0a49fe0a4bee0a489e0a495e0a58b[0]<0 or ue0a49fe0a4bee0a489e0a495e0a58b[1]<0 or ue0a49fe0a4bee0a489e0a495e0a58b[1]>30 or ue0a49fe0a4bee0a489e0a495e0a58b[1]>30 :#68
		ue0a49ae0a4b2e0a4bee0a489 = 0#69

ue0a4b8e0a4ace0a588e0a4aee0a4bfe0a4b2e0a4bee0a489()#0
while ue0a49ae0a4b2e0a4bee0a489:#74
	ue0a4b8e0a4ace0a588e0a49ae0a4bfe0a4a4e0a58de0a4b0e0a495e0a58be0a4b0()#0
	ue0a487e0a4a8e0a58de0a4aae0a581e0a49fe0a495e0a587e0a49be0a4b9e0a587e0a4b0()#0
	ue0a4b8e0a4b0e0a58de0a4aae0a4b2e0a4bee0a488e0a4aee0a4bfe0a4b2e0a4bee0a489()#0
	ue0a4b8e0a581e0a4a4()#0


