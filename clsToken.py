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
		#return "<Token: %s %r %d %d>" % (self.type, self.value,self.lineno,self.lexpos)

class TknUSE(Token):
	ER=re.compile(r'use\b')

class TknBEGIN(Token):
	ER=re.compile(r'begin\b')

class TknIN(Token):
	ER=re.compile(r'in\b')

class TknEND(Token):
	ER=re.compile(r'end\b')

class TknFUNCTION(Token):
	ER=re.compile(r'function\b')

class TknRETURN(Token):
	ER=re.compile(r'return\b')

class TknIF(Token):
	ER=re.compile(r'if\b')

class TknTHEN(Token):
	ER=re.compile(r'then\b')

class TknFOR(Token):
	ER=re.compile(r'for\b')

class TknELSE(Token):
	ER=re.compile(r'else\b')

class TknDO(Token):
	ER=re.compile(r'do\b')

class TknWHILE(Token):
	ER=re.compile(r'while\b')

class TknNUMBER(Token):
	ER=re.compile(r'number\b')

class TknBOOLEAN(Token):
	ER=re.compile(r'boolean\b')

class TknTRUE(Token):
	ER=re.compile(r'true\b')

class TknFALSE(Token):
	ER=re.compile(r'false\b')

class TknMATRIX(Token):
	ER=re.compile(r'matrix\b')

class TknROW(Token):
	ER=re.compile(r'row\b')

class TknCOL(Token):
	ER=re.compile(r'col\b')

class TknPRINT(Token):
	ER=re.compile(r'print\b')

class TknSET(Token):
	ER=re.compile(r'set\b')

class TknNOT(Token):
	ER=re.compile(r'not\b')

class TknMMOD(Token):
	ER=re.compile(r'\.mod\.')

class TknMDIV(Token):
	ER=re.compile(r'\.div\.')

class TknMSUMA(Token):
	ER=re.compile(r'\.\+\.')

class TknMMENOS(Token):
	ER=re.compile(r'\.\-\.')

class TknMAST(Token):
	ER=re.compile(r'\.\*\.')

class TknMSLASH(Token):
	ER=re.compile(r'\./\.')

class TknMPORCENTAJE(Token):
	ER=re.compile(r'\.%\.')

class TknPUNTOYCOMA(Token):
	ER=re.compile(r';')

class TknDOSPUNTOS(Token):
	ER=re.compile(r':')

class TknIGUAL2(Token):
	ER=re.compile(r'==')

class TknDISTINTO(Token):
	ER=re.compile(r'/=')

class TknMAYORIGUAL(Token):
	ER=re.compile(r'>=')

class TknMENORIGUAL(Token):
	ER=re.compile(r'<=')

class TknMAYORQUE(Token):
	ER=re.compile(r'>')

class TknMENORQUE(Token):
	ER=re.compile(r'<')

class TknIGUAL(Token):
	ER=re.compile(r'=')

class TknPUNTO(Token):
	ER=re.compile(r'\.')

class TknCOMA(Token):
	ER=re.compile(r'\,')

class TknDIV(Token):
	ER=re.compile(r'div\b')

class TknMOD(Token):
	ER=re.compile(r'mod\b')

class TknSUMA(Token):
	ER=re.compile(r'\+')

class TknMENOS(Token):
	ER=re.compile(r'-\b')

class TknAST(Token):
	ER=re.compile(r'\*')

class TknSLASH(Token):
	ER=re.compile(r'/')

class TknAND(Token):
	ER=re.compile(r'&')

class TknOR(Token):
	ER=re.compile(r'\|')

class TknPORCENTAJE(Token):
	ER=re.compile(r'%')

class TknPARENTESISABRE(Token):
	ER=re.compile(r'\(')

class TknPARENTESISCIERRA(Token):
	ER=re.compile(r'\)')

class TknCORCHETEABRE(Token):
	ER=re.compile(r'\[')

class TknCORCHETECIERRA(Token):
	ER=re.compile(r'\]')

class TknLLAVESABRE(Token):
	ER=re.compile(r'\{')

class TknLLAVESCIERRA(Token):
	ER=re.compile(r'\}')

class TknSTRING(Token):
	ER=re.compile(r'".*?"')#non-greedy
	#ER=re.compile('/"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"')#probar luego

class TknCOMILLASIMPLE(Token):
	ER=re.compile(r'\'')

class TknNUMERO(Token):
	ER=re.compile(r'[-+]?(\d+(\.\d+)?)')

class TknID(Token):
	ER=re.compile(r'[A-Za-z]\w*')

