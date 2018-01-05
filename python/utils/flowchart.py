#encoding=UTF8
"""
pydot example 2
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot
import re

graph = pydot.Dot(graph_type='digraph', nodesep=2)

#read from rhee file
rhee_text = []

text = open("Rhee_Files/5_hanoi.rhee", 'r').read().decode('utf-8')
# print type(text)
#seperate the function definitions into a list
funcs = list(re.findall(u"(काम.*?मका)",text,re.MULTILINE|re.DOTALL))
# print funcs[0]
for f in funcs:
    text = text.replace(funcs[0],'')
# exit(0)


for l in text.split('\n'):
    l = l.strip()
    if l == '': continue
    if l[0:2] == '//': continue
    rhee_text.append(l)

# print '\n'.join(rhee_text)

rhee_text.insert(0, u'शुरू')
rhee_text.append(u'अन्त्य')
nodes = []
edges = []

jaba_list = []

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

    if current_line[0:2] == u'बज':
        graph.add_edge(pydot.Edge(jaba_list.pop(-1), node,dir='both', label=u'असत्य', fontname='Sans-Serif'))
    # graph.add_node(node)
    nodes.append(node)

for n in nodes:
    graph.add_node(n)

for i in range(len(nodes)-1):
    graph.add_edge(pydot.Edge(nodes[i], nodes[i+1]))



# graph.add_node(node_a)
graph.write_png("flowchart.png")


# # node_a = pydot.Node("Node A", style="filled", fillcolor="red")
# node_a = pydot.Node("Node A")
#
# # neat, huh? Let us create the rest of the nodes!
# node_b = pydot.Node(u"Node मेरो", fontname='Sans-Serif')
# node_c = pydot.Node("Node C")
# node_d = pydot.Node("Node D")
#
# #ok, now we add the nodes to the graph
# graph.add_node(node_a)
# graph.add_node(node_b)
# graph.add_node(node_c)
# graph.add_node(node_d)
#
# # and finally we create the edges
# # to keep it short, I'll be adding the edge automatically to the graph instead
# # of keeping a reference to it in a variable
# graph.add_edge(pydot.Edge(node_a, node_b))
# graph.add_edge(pydot.Edge(node_b, node_c))
# graph.add_edge(pydot.Edge(node_c, node_d))
# # but, let's make this last edge special, yes?
# graph.add_edge(pydot.Edge(node_d, node_a, label="and back we go again", labelfontcolor="#009933", fontsize="10.0", color="blue"))
#
# # and we are done
# graph.write_png('example3_graph.png')
#
