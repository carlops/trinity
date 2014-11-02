'''
Analizador Lexicografico del Lenguaje Trinity
Creado:26/09/14
Ult.Mod:6/10/14
Autores:
	Carlo Polisano S. 0910672
	Alejandro Guevara 0910971
'''
import re
from clsToken import *
#from clsToken import PLYCompatToken

class PLYCompatLexer(object):
	def __init__(self, text):
		self.text = text
		self.token_stream = iter(Lexer(text))
		#self.token_stream = Lexer(text)
		
	def token(self):
		try:
			#return PLYCompatToken(self.token_stream.next())
			unToken = PLYCompatToken(self.token_stream.next())
			#print 'in token: ', unToken.type
			return unToken
			#return self.token_stream
		except StopIteration:
			return None
		
class PLYCompatToken:
        def __init__(self, token):
            self.type = token.type
            self.value = token.value
            self.lineno = token.lineno
            self.lexpos = token.lexpos
	#def input(self,text):
		#pass

def Lexer(text):
	TokenList = [] # Lista de Tokens
	for i in Token.__subclasses__():
		TokenList.append(i)

	Ignorar = re.compile(r"(?P<ESPACIO> )|(?P<TAB>\t)")

	NumLinea = 1 # Contador Numero de linea
	NumCol = 1 # Contador Numero de Columnas

	error=False
	TknEncontrados=list()
	ErrEncontrados=list()

	# Leyendo
	while len(text)>0:
		m = Ignorar.match(text)
		if m: # Encontre algo que debo ignorar
			text= text[len(m.group(0)):] # Se lo quito al text
			NumCol = NumCol + len(m.group(0)) # Aumento NumCol
			continue
		
		m = re.match(r'\n',text)
		if m: # Encontre un fin de linea
			text= text[len(m.group(0)):] # Se lo quito al text
			NumLinea = NumLinea + 1
			NumCol = 1
			continue
		
		m = re.match(r'#',text)
		if m: # Encontre un comentario de linea
			i = re.match(r'(.)*\n',text) # Encuentro en final de la linea de comentarios
			if i == None: #si finaliza el archivo sin \n
				break
			text= text[len(i.group(0)):] # Se lo quito al text
			NumLinea = NumLinea + 1
			NumCol = 1
			continue
				
		for tk in TokenList:
			m = tk.ER.match(text)
			if m:
				Newtk = tk(NumLinea,NumCol,m.group(0)) # Creo el Token
				TknEncontrados.append(Newtk)
				text= text[len(m.group(0)):] # Se lo quito al text
				NumCol = NumCol + len(m.group(0))
				break
		
		if not m:# No encontro una expresion regular, Error Lexicografico
			i = re.match(r'.',text)
			ErrEncontrados.append([i.group(0),NumLinea,NumCol])
			text= text[len(i.group(0)):]
			NumCol = NumCol + len(i.group(0))
			error=True

	#for i in TknEncontrados:
		#print("{} en la  {}, columna {}: {}".format(i.type,i.lineno,i.lexpos,i.value))
	#print 

	if not error:
		return TknEncontrados
	else:
		for i in ErrEncontrados:
			print("Error:{} encontrado en fila {} y columna {}".format(i[0],i[1],i[2]))
		print("Ocurrio al menos un error Lexicografico. Deteniendo la ejecucion")
		exit(1)

if __name__ == '__main__':
	
	archivo = open(sys.argv[1], 'r')

	text = archivo.read() # Todo el archivo en un solo string

	# Cerrando Archivo
	archivo.close()
	
	lx=PLYCompatLexer(text)
    