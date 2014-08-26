#encoding=UTF8

from Lexer import RheeLexer
L = RheeLexer()
L.build()

keywords = [
    u'र',
    u'वा',
    u'यदि',
    u'भए',
    u'नभए',
    u'लेख',
    u'अथवा',
    u'लेउ',
    u'दिय',
    u'सबै',
    u'देखि',
    u'बैस',
    u'जब',
    u'बज',
    u'सम्म',
    u'छैन',
    u'छ',
    u'काम',
    u'मका',
    u'पठाउ',
    u'मा',
    u'बाट',
    u'बन्दगर',
    u'देखाउ',
    u'लुकाउ',
    u'बनाउ',
    u'कोर',
    u'मेटाउ',
    u'हटाउ',
    u'बाहिर',
    u'अर्को',
    u'शुन्य',
    u'चोटि',
    u'टिचो',
    u'खाका',
    U'काखा',
    ]

rhee_block_start = [
  	'YEDI',
    'SABAI',
    'JABA',
    'KAAM',
    'CHOTI',
    'KHAKA',
]

rhee_block_end = [
    'KAKHA',
    'TICHO',
    'MAKA',
    'BAJA',
    'BAISA',
    'DIYE',
]

def GetAutoCompleteList(text, line):
    L.lexer.lineno = 0
    L.lexer.lexpos = 0
    tokens = L.tokenize(text)

    #Goal is to find all globals and all other variables upto line 'line'

    #first find all globals
    scope = 0
    global_vars = []
    local_vars = []
    functions_classes = []
    for i, t in enumerate(tokens):
        if t.lineno -1 >= line: break
        id = t.type
        if id in rhee_block_start:
            scope += 1
        elif id in rhee_block_end:
            scope -= 1
        else:
            if id == 'IDENTIFIER':

                if i-1 >=0 and tokens[i-1].type=='KAAM' or \
                i-1 >=0 and tokens[i-1].type=='KHAKA':
                    functions_classes.append(t.value)
                else:

                    if i+1 < len(tokens) and tokens[i+1].type == 'LPARA': continue #function call

                    if scope == 0:
                        global_vars.append(t.value)
                    else:
                        local_vars.append(t.value)


    global_vars = list(set(global_vars))
    local_vars = list(set(local_vars))
    functions_classes = list(set(functions_classes))
    return global_vars, local_vars, functions_classes




