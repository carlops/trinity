'''
Clase de los Tokens del Analizador Lexicografico del Lenguaje Trinity
Creado:26/09/14
Ult.Mod:26/09/14
Autores:
	Carlo Polisano S. 0910672
	Alejandro Guevara 0910971
'''
import re

class Token(object):
	def __init__(self, fila, col, code):
		self.type = self.__class__.__name__
		self.value = code
		self.lineno = fila
		self.lexpos = col
		
#class Token(object):
	#def __init__(self, fila, col, code):
		#self.name = self.__class__.__name__
		#self.fila = fila
		#self.col = col
		#self.code = code

#class PLYCompatToken(object):
	#def __init__(self, tk):
		#self.type = 
		#self.value = code
		#self.lineno = fila
		#self.lexpos = col
	
	def __repr__(self):
		return self.__class__.__name__
		return "<Token: %s %r %d %d>" % (self.type, self.value,self.lineno,self.lexpos)

class t_USE(Token):
	ER=re.compile(r'use\b')
	#r'use\b'

class t_BEGIN(Token):
	ER=re.compile(r'begin\b')
	#r'begin\b'

class t_IN(Token):
	ER=re.compile(r'in\b')
	#r'in\b'

class t_END(Token):
	ER=re.compile(r'end\b')
	#r'end\b'

class t_FUNCTION(Token):
	ER=re.compile(r'function\b')
	#r'function\b'

class t_RETURN(Token):
	ER=re.compile(r'return\b')
	#r'return\b'

class t_IF(Token):
	ER=re.compile(r'if\b')
	#r'if\b'

class t_THEN(Token):
	ER=re.compile(r'then\b')
	#r'then\b'

class t_FOR(Token):
	ER=re.compile(r'for\b')
	#r'for\b'

class t_ELSE(Token):
	ER=re.compile(r'else\b')
	#r'else\b'

class t_DO(Token):
	ER=re.compile(r'do\b')
	#r'do\b'

class t_WHILE(Token):
	ER=re.compile(r'while\b')
	#r'while\b'

class t_NUMBER(Token):
	ER=re.compile(r'number\b')
	#r'number\b'

class t_BOOLEAN(Token):
	ER=re.compile(r'boolean\b')
	#r'boolean\b'

class t_TRUE(Token):
	ER=re.compile(r'true\b')
	#r'true\b'

class t_FALSE(Token):
	ER=re.compile(r'false\b')
	#r'false\b'

class t_MATRIX(Token):
	ER=re.compile(r'matrix\b')
	#r'matrix\b'

class t_ROW(Token):
	ER=re.compile(r'row\b')
	#r'row\b'

class t_COL(Token):
	ER=re.compile(r'col\b')
	#r'col\b'

class t_PRINT(Token):
	ER=re.compile(r'print\b')
	#r'print\b'

class t_SET(Token):
	ER=re.compile(r'set\b')
	#r'set\b'

class t_NOT(Token):
	ER=re.compile(r'not\b')
	#r'not\b'

class t_MMOD(Token):
	ER=re.compile(r'\.mod\.')
	#r'\.mod\.'

class t_MDIV(Token):
	ER=re.compile(r'\.div\.')
	#r'\.div\.'

class t_MSUMA(Token):
	ER=re.compile(r'\.\+\.')
	#r'\.\+\.'

class t_MMENOS(Token):
	ER=re.compile(r'\.\-\.')
	#r'\.\-\.'

class t_MAST(Token):
	ER=re.compile(r'\.\*\.')
	#r'\.\*\.'

class t_MSLASH(Token):
	ER=re.compile(r'\./\.')
	#r'\./\.'

class t_MPORCENTAJE(Token):
	ER=re.compile(r'\.%\.')
	#r'\.%\.'

class t_PUNTOYCOMA(Token):
	ER=re.compile(r';')
	#r';'

class t_DOSPUNTOS(Token):
	ER=re.compile(r':')
	#r':'

class t_IGUAL2(Token):
	ER=re.compile(r'==')
	#r'=='

class t_DISTINTO(Token):
	ER=re.compile(r'/=')
	#r'/='

class t_MAYORIGUAL(Token):
	ER=re.compile(r'>=')
	#r'>='

class t_MENORIGUAL(Token):
	ER=re.compile(r'<=')
	#r'<='

class t_MAYORQUE(Token):
	ER=re.compile(r'>')
	#r'>'

class t_MENORQUE(Token):
	ER=re.compile(r'<')
	#r'<'

class t_IGUAL(Token):
	ER=re.compile(r'=')
	#r'='

class t_PUNTO(Token):
	ER=re.compile(r'\.')
	#r'\.'

class t_COMA(Token):
	ER=re.compile(r'\,')
	#r'\,'

class t_DIV(Token):
	ER=re.compile(r'div\b')
	#r'div\b'

class t_MOD(Token):
	ER=re.compile(r'mod\b')
	#r'mod\b'

class t_SUMA(Token):
	ER=re.compile(r'\+')
	#r'\+'

class t_MENOS(Token):
	ER=re.compile(r'-\b')
	#r'-\b'

class t_AST(Token):
	ER=re.compile(r'\*')
	#r'\*'

class t_SLASH(Token):
	ER=re.compile(r'/')
	#r'/'

class t_AND(Token):
	ER=re.compile(r'&')
	#r'&'

class t_OR(Token):
	ER=re.compile(r'\|')
	#r'\|'

class t_PORCENTAJE(Token):
	ER=re.compile(r'%')
	#r'%'

class t_PARENTESISABRE(Token):
	ER=re.compile(r'\(')
	#r'\('

class t_PARENTESISCIERRA(Token):
	ER=re.compile(r'\)')
	#r'\)'

class t_CORCHETEABRE(Token):
	ER=re.compile(r'\[')
	#r'\['

class t_CORCHETECIERRA(Token):
	ER=re.compile(r'\]')
	#r'\]'

class t_LLAVESABRE(Token):
	ER=re.compile(r'\{')
	#r'\{'

class t_LLAVESCIERRA(Token):
	ER=re.compile(r'\}')
	#r'\}'

class t_STRING(Token):
	ER=re.compile(r'".*?"')
	#r'".*?"'#non-greedy
	#ER=re.compile('/"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"')
	'/"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'#probar luego

class t_COMILLASIMPLE(Token):
	ER=re.compile(r'\'')
	#r'\''

class t_NUMERO(Token):
	ER=re.compile(r'[-+]?(\d+(\.\d+)?)')
	#r'[-+]?(\d+(\.\d+)?)'

class t_ID(Token):
	ER=re.compile(r'[A-Za-z]\w*')
	#r'[A-Za-z]\w*'

