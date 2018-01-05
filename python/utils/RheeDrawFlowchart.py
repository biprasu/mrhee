#encoding=UTF8
"""
pydot example 2
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot
import re
import os

def draw_function(text, dirname):
    firstline = text[:text.find('\n')]
    funcname = re.findall(ur'काम ([^\(]+)', firstline)[0]
    draw_body(text, '', '', funcname+u'.png', dirname)

def draw_classes():
    pass

def draw_body(text, start, end, filename, dirname):
    graph = pydot.Dot(graph_type='digraph', nodesep=2)
    rhee_text = []
    for l in text.split('\n'):
        l = l.strip()
        if l == '': continue
        if l[0:2] == '//': continue
        r = re.findall(r'//.+$', l)
        for v in r:
            l = l.replace(v,'')
        rhee_text.append(l.strip())

    # print '\n'.join(rhee_text)

    rhee_text.insert(0, start)
    rhee_text.append(end)
    nodes = []
    edges = []

    jaba_list = []
    yedi_list = []
    sabai_list = []
    choti_list = []
    athawa_list = []
    conditional_list = []

    while rhee_text:
        if rhee_text[0] == '':
            rhee_text.pop(0)
            continue
        current_line = rhee_text.pop(0)
        s = ''
        if current_line[-3:] == u'लेख' or current_line[-3:]==u'लेउ':
            shape='parallelogram'
        elif current_line[0:3] == u'यदि' or current_line[0:4] == u'अथवा' or current_line[0:2] == u'जब':
            shape='diamond'
        elif current_line == u'अन्त्य'or current_line == u'शुरू':
            shape='oval'
        else:
            shape='rectangle'
        node = pydot.Node(current_line, fontname='Sans-Serif', shape=shape)

        if current_line[0:2] == u'जब':
            jaba_list.append(node)
            conditional_list.append(node)
        if current_line[0:3] == u'यदि':
            yedi_list.append(node)
            conditional_list.append(node)
        if current_line[0:3] == u'सबै':
            sabai_list.append(node)
        if re.match(ur'[०१२३४५६७८९]+ चोटि', current_line):
            choti_list.append(node)
        if current_line[0:4] == u'अथवा':
            athawa_list.append(node)
            conditional_list.append(node)


        if current_line[0:2] == u'बज':
            graph.add_edge(pydot.Edge(jaba_list.pop(-1), node,dir='both', label=u'असत्य', fontname='Sans-Serif'))

        if current_line[0:3] == u'दिय':
            graph.add_edge(pydot.Edge(yedi_list.pop(-1), node,dir='forward', label=u'असत्य', fontname='Sans-Serif'))

        if current_line[0:3] == u'बैस':
            graph.add_edge(pydot.Edge(sabai_list.pop(-1), node,dir='both', fontname='Sans-Serif'))

        if current_line[0:4] == u'टिचो':
            graph.add_edge(pydot.Edge(choti_list.pop(-1), node,dir='both', fontname='Sans-Serif'))

        if current_line[0:4] == u'अथवा':
            if len(athawa_list)>1:
                graph.add_edge(pydot.Edge(athawa_list.pop(-2), node,dir='forward',label=u'असत्य', fontname='Sans-Serif'))


        # graph.add_node(node)
        nodes.append(node)

    for n in nodes:
        graph.add_node(n)

    for i in range(len(nodes)-1):
        if nodes[i] in conditional_list:
            graph.add_edge(pydot.Edge(nodes[i], nodes[i+1], label = u'सत्य', fontname='Sans-Serif'))
        else:
            graph.add_edge(pydot.Edge(nodes[i], nodes[i+1]))


    # graph.add_node(node_a)
    graph.write_png(os.path.join(dirname, filename), encoding="utf-8" )


def draw_file(filename, dirname = '.'):
    #read from rhee file
    if not filename or not dirname: return
    text = open(filename, 'r').read().decode('utf-8')
    # print type(text)

    if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
        for the_file in os.listdir(unicode(dirname)):
            file_path = os.path.join(dirname, the_file)
            try:
                if os.path.isfile(file_path):
                    if file_path[-3:] == 'png':
                        os.unlink(file_path)
            except Exception, e:
                pass

    #seperate the function definitions into a list
    funcs = list(re.findall(ur"^\s*(काम.*?मका)\s*$",text,re.MULTILINE|re.DOTALL))
    classes = list(re.findall(ur"^\s*(खाका.*?काखा)\s*$",text,re.MULTILINE|re.DOTALL))
    # print funcs[0]
    for f in funcs+classes:
        text = text.replace(f,'')

    filenameonly = os.path.split(filename)[-1]
    filenamewithoutextension = os.path.splitext(filenameonly)[0]
    draw_body(text, u'शुरू', u'अन्त्य', filenamewithoutextension+'.png', dirname)

    for f in funcs:
        draw_function(f, dirname)
    # draw_body(text)
    # exit(0)


if __name__ == '__main__':
    draw_file("Rhee_Files/8puzzle.rhee", "flowcharts")