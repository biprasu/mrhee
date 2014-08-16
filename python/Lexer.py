#encoding=UTF8

'''
Set of regular expression defining a lexer for Rhee Programming Language
'''

import ply.lex as lex

tokens = []

class RheeLexer:
	reserved = {
	u'र'  : 'RA',
    u'वा' : 'WA',
    
	u'यदि' : 'YEDI',
    u'भए' : 'BHAE',
    u'नभए'  : 'NABHAE',
    u'लेख' : 'LEKHA',
    u'अथवा' : 'ATHAWA',
    u'लेउ' : 'LEU',
    u'दिय' : 'DIYE',
    u'सबै' : 'SABAI',
    u'देखि' : 'DEKHI',
    u'बैस' : 'BAISA',
    u'जब' : 'JABA',
    u'बज' : 'BAJA',
    u'सम्म' : 'SAMMA',
    u'छैन' : 'CHHAINA',
    u'छ' : 'CHHA',
    u'काम' : 'KAAM',
    u'मका' : 'MAKA',
    u'पठाउ' : 'PATHAU',

    u'मा' : 'MA',
    u'बाट' : 'BATA',
    u'बन्दगर' :'BANDAGARA',
    u'देखाउ' : 'DEKHAU',
    u'लुकाउ' : 'LUKAU',
    u'बनाउ' : 'BANAU',
    u'कोर' : 'KORA',
    u'मेटाउ' : 'METAU',
    u'हटाउ' : 'HATAU',
    
    u'शुन्य' : 'SUNYA',
    u'साचो'	: 'SACHO',
    u'झुटो'	: 'JHUTO',

    u'बाहिर' : 'BAHIRA',
    u'अर्को': 'ARKO',
    u'चोटि' : 'CHOTI',
    u'टिचो' : 'TICHO',
    u'खाका'	: 'KHAKA',
    U'काखा'	: 'KAKHA',
	}
	tokens  = reserved.values()
	tokens += ['IDENTIFIER', 'DECIMALINTEGER', 'OCTALINTEGER', 'HEXAINTEGER', 'FLOAT', 'IMAGNUMBER', 'STRING']
	tokens += ['PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'POWER', 'MODULUS', 'LPARA', 'RPARA', 'LGPARA', 'RGPARA']
	tokens += ['GE', 'LE', 'EQ', 'NE', 'GT', 'LT', 'AI', 'SI', 'MI', 'DI']
	tokens += ['ASSIGNMENT', 'COMMA', 'SEMICOLON', 'COLON', 'QUESTION', 'NEWLINE']
	tokens += ['BOGUS', 'DOT']

	# we support these range of devanagari script
	digit 		= ur'([\u0966-\u096F])'
	nondigit 	= ur'([\u0900-\u0965])'

	# mathematical symbols
	t_PLUS 	= ur'\+'
	t_MINUS = ur'\-'
	t_DIVIDE = ur'/'
	t_TIMES = ur'\*'
	t_POWER = ur'\^'
	t_MODULUS = ur'\%'

	# paranthesis
	t_LPARA = ur'\('
	t_RPARA = ur'\)'
	 
	t_LGPARA = ur'\['
	t_RGPARA = ur'\]'
	 
	# logical
	t_GE = ur'>='
	t_LE = ur'<='
	t_EQ = ur'=='
	t_NE = ur'!='
	t_GT = ur'>'
	t_LT = ur'<'

	# Incremental
	t_AI = ur'\+='
	t_SI = ur'-='
	t_MI = ur'\*='
	t_DI = ur'/='

	# assignment
	t_ASSIGNMENT 	= ur'='
	t_COMMA 		= ur','
	t_SEMICOLON 	= ur';'
	t_COLON 		= ur':'
	t_QUESTION 		= ur'\?'

	t_DOT = ur'\.'

	
	def t_IDENTIFIER(self, token):
		ur'[\u0900-\u0965_][\u0900-\u0965_०-९\u200d]*'
		token.type = self.reserved.get(token.value,'IDENTIFIER')
		return token

	# number system begins here
	def t_HEXAINTEGER(self, token):
		ur'\u0966[xX][\u0966-\u096FABCDEFabcdef]+'
		return token

	def t_OCTALINTEGER(self, token):
		ur'\u0966[\u0966-\u096D]+'
		return token

	def t_IMAGNUMBER(self, token):
		ur'[\u0966-\u096F]*(\.[\u0966-\u096F]+([eE][+-]?[\u0966-\u096F]+)?)?[ijIJ]'
		if len(token.value) == 1:
			token.value = '1'
		else:
			token.value = token.value[:-1]
		return token

	def t_FLOAT(self, token):
		ur'[\u0966-\u096F]*\.[\u0966-\u096F]+([eE][+-]?[\u0966-\u096F]+)?'
		return token
	
	def t_DECIMALINTEGER(self, token):
		ur'([\u0967-\u096F][\u0966-\u096F]*)|\u0966'
		return token
	
	# end number system



	#string
	def t_STRING(self, token):
		ur'("[^"]*")|(\'[^\']*\')'
		token.value = token.value[1:-1]
		token.lexer.lineno += token.value.count('\n')
		return token

	def t_MATHFUNC(self, token):
		ur'(?:sin)|(?:cos)|(?:tan)|(?:asin)|(?:acos)|(?:atan)|(?:log)|(?:alog)'
		token.type = "IDENTIFIER"
		return token


	def t_NEWLINE(self, token):
		ur'\n+'
		token.lexer.lineno += token.value.count('\n')
		return token

	def t_COMMENT(self, token):
		ur'(//.*)|(/\*[^\(*/)]*\*/)'
		token.lexer.lineno += token.value.count('\n')

	t_ignore = r' 	'


	def t_error(self, token):
		print "Warning(Lexer): Illegal character " + token.value[0] + " !!"
		token.lexer.skip(1)


	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

	def test(self, data):
		'Test the lexer with input data'
		self.lexer.input(data)
		while True:
			tok = self.lexer.token()
			if not tok: break
			print tok

	def get_tokens(self): 	return self.tokens
	def get_lexer(self):	return self.lexer



# @TODO octal and hexa check in parser