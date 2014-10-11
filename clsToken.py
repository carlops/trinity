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
	#def __ini_(self, fila, col, code):
		#self.name = self.__class__.__name__
		#self.fila = fila
		#self.col = col
		#self.code = code

#class PLYCompatToken(object):
	#def __ini_(self, tk):
		#self.type = 
		#self.value = code
		#self.lineno = fila
		#self.lexpos = col
	
	#def __repr__(self):
		#return self.__class__.__name__
		#return "<Token: %s %r %d %d>" % (self.type, self.value,self.lineno,self.col)

class USE(Token):
	ER=re.compile(r'use\b')
	#r'use\b'

class BEGIN(Token):
	ER=re.compile(r'begin\b')
	#r'begin\b'

class IN(Token):
	ER=re.compile(r'in\b')
	#r'in\b'

class END(Token):
	ER=re.compile(r'end\b')
	#r'end\b'

class FUNCTION(Token):
	ER=re.compile(r'function\b')
	#r'function\b'

class RETURN(Token):
	ER=re.compile(r'return\b')
	#r'return\b'

class IF(Token):
	ER=re.compile(r'if\b')
	#r'if\b'

class THEN(Token):
	ER=re.compile(r'then\b')
	#r'then\b'

class FOR(Token):
	ER=re.compile(r'for\b')
	#r'for\b'

class ELSE(Token):
	ER=re.compile(r'else\b')
	#r'else\b'

class DO(Token):
	ER=re.compile(r'do\b')
	#r'do\b'

class WHILE(Token):
	ER=re.compile(r'while\b')
	#r'while\b'

class NUMBER(Token):
	ER=re.compile(r'number\b')
	#r'number\b'

class BOOLEAN(Token):
	ER=re.compile(r'boolean\b')
	#r'boolean\b'

class TRUE(Token):
	ER=re.compile(r'true\b')
	#r'true\b'

class FALSE(Token):
	ER=re.compile(r'false\b')
	#r'false\b'

class MATRIX(Token):
	ER=re.compile(r'matrix\b')
	#r'matrix\b'

class ROW(Token):
	ER=re.compile(r'row\b')
	#r'row\b'

class COL(Token):
	ER=re.compile(r'col\b')
	#r'col\b'

class PRINT(Token):
	ER=re.compile(r'print\b')
	#r'print\b'

class SET(Token):
	ER=re.compile(r'set\b')
	#r'set\b'

class NOT(Token):
	ER=re.compile(r'not\b')
	#r'not\b'

class MMOD(Token):
	ER=re.compile(r'\.mod\.')
	#r'\.mod\.'

class MDIV(Token):
	ER=re.compile(r'\.div\.')
	#r'\.div\.'

class MSUMA(Token):
	ER=re.compile(r'\.\+\.')
	#r'\.\+\.'

class MMENOS(Token):
	ER=re.compile(r'\.\-\.')
	#r'\.\-\.'

class MAST(Token):
	ER=re.compile(r'\.\*\.')
	#r'\.\*\.'

class MSLASH(Token):
	ER=re.compile(r'\./\.')
	#r'\./\.'

class MPORCENTAJE(Token):
	ER=re.compile(r'\.%\.')
	#r'\.%\.'

class PUNTOYCOMA(Token):
	ER=re.compile(r';')
	#r';'

class DOSPUNTOS(Token):
	ER=re.compile(r':')
	#r':'

class IGUAL2(Token):
	ER=re.compile(r'==')
	#r'=='

class DISTINTO(Token):
	ER=re.compile(r'/=')
	#r'/='

class MAYORIGUAL(Token):
	ER=re.compile(r'>=')
	#r'>='

class MENORIGUAL(Token):
	ER=re.compile(r'<=')
	#r'<='

class MAYORQUE(Token):
	ER=re.compile(r'>')
	#r'>'

class MENORQUE(Token):
	ER=re.compile(r'<')
	#r'<'

class IGUAL(Token):
	ER=re.compile(r'=')
	#r'='

class PUNTO(Token):
	ER=re.compile(r'\.')
	#r'\.'

class COMA(Token):
	ER=re.compile(r'\,')
	#r'\,'

class DIV(Token):
	ER=re.compile(r'div\b')
	#r'div\b'

class MOD(Token):
	ER=re.compile(r'mod\b')
	#r'mod\b'

class SUMA(Token):
	ER=re.compile(r'\+')
	#r'\+'

class MENOS(Token):
	ER=re.compile(r'-\b')
	#r'-\b'

class AST(Token):
	ER=re.compile(r'\*')
	#r'\*'

class SLASH(Token):
	ER=re.compile(r'/')
	#r'/'

class AND(Token):
	ER=re.compile(r'&')
	#r'&'

class OR(Token):
	ER=re.compile(r'\|')
	#r'\|'

class PORCENTAJE(Token):
	ER=re.compile(r'%')
	#r'%'

class PARENTESISABRE(Token):
	ER=re.compile(r'\(')
	#r'\('

class PARENTESISCIERRA(Token):
	ER=re.compile(r'\)')
	#r'\)'

class CORCHETEABRE(Token):
	ER=re.compile(r'\[')
	#r'\['

class CORCHETECIERRA(Token):
	ER=re.compile(r'\]')
	#r'\]'

class LLAVESABRE(Token):
	ER=re.compile(r'\{')
	#r'\{'

class LLAVESCIERRA(Token):
	ER=re.compile(r'\}')
	#r'\}'

class STRING(Token):
	ER=re.compile(r'".*?"')
	#r'".*?"'#non-greedy
	#ER=re.compile('/"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"')
	'/"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'#probar luego

class COMILLASIMPLE(Token):
	ER=re.compile(r'\'')
	#r'\''

class NUMERO(Token):
	ER=re.compile(r'(\d+(\.\d+)?)')
	#r'[-+]?(\d+(\.\d+)?)'

class ID(Token):
	ER=re.compile(r'[A-Za-z]\w*')
	#r'[A-Za-z]\w*'

