#!/usr/bin/env python
'''
Analizador Sintactico del Lenguaje Trinity
Creado:6/10/14
Ult.Mod:6/10/14
Autores:
	Carlo Polisano S. 0910672
	Alejandro Guevara 0910971
'''
from clsToken import Token
import ply.yacc as yacc
import re
import sys

class Function:
	def __init__(self,Identificador, parametros, tipo, instrucciones):
		self.Identificador = Identificador
		self.parametros = parametros
		self.tipo = tipo
		self.instrucciones = instrucciones
		
	def show(self, depth):
		print('  '*depth + 'Funcion:')
		self.Identificador.show(depth+1)
		print('  '*(depth+1) + 'Parametros:')
		self.parametros.show(depth+2)
		print('  '*(depth+1) + 'Retorna Tipo:')
		self.tipo.show(depth+2)
		print('  '*(depth+1) + 'BEGIN:')
		self.instrucciones(depth+2)
		print('  '*(depth+1) + 'END:')
		
class Program:
	def __init__(self,cuerpo):
		self.cuerpo=cuerpo

	def show(self, depth):
		#print 'PROGRAM'
		self.cuerpo.show(depth)
		#print 'END'
		
class Statement:
	pass
	
class ListasSt_Dcl(Statement):
	def __init__(self, AnStatement, ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		
	def show(self, depth):
		if self.ManyStatements == None:
			self.AnStatement.show(depth)
		else:
			self.AnStatement.show(depth)
			self.ManyStatements.show(depth)

class Bloque(Statement):
	def __init__(self,declaraciones,instrucciones):
		self.declaraciones=declaraciones
		self.instrucciones=instrucciones
		
	def show(self,depth):
		print('  '*depth+'USE:')
		self.declaraciones.show(depth+1)
		print('  '*depth+'IN:')
		self.instrucciones.show(depth+1)
		print('  '*depth+'END')
		
#---------ESTRUCTURAS DE CONTROL-----------------------
class instruccion_IF(Statement):
	def __init__(self,condicion,instrucciones,instruccionesElse):
		self.condicion = condicion
		self.instrucciones = instrucciones
		self.instruccionesElse = instruccionesElse
		
	def show(self, depth):
		print('  '*depth+'IF:')
		self.condicion.show(depth+1)
		print('  '*depth + 'THEN')
		self.instrucciones.show(depth+1)
		if self.instruccionesElse != None:
			print('  '*depth + 'ELSE')
			self.instruccionesElse.show(depth+1)
		print('  '*depth + 'END')
		
class instruccion_FOR(Statement):
	def __init__(self,ID,estructura,instrucciones):
		self.ID= ID
		self.estructura = estructura
		self.instrucciones = instrucciones
		
	def show(self,depth):
		print('  '*depth+'FOR:')
		self.ID.show(depth+1)
		print('  '*depth + 'IN')
		self.estructura.show(depth+1)
		print('  '*depth + 'DO')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
class instruccion_WHILE(Statement):
	def __init__(self, condicion,instrucciones):
		self.condicion = condicion
		self.instrucciones = instrucciones
		
	def show(self, depth):
		print('  '*depth+'WHILE:')
		self.condicion.show(depth+1)
		print('  '*depth + 'DO')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
class Read(Statement):
	def __init__(self, Identificador):
		self.Identificador = Identificador
	def show(self, depth):
		print ('  '*depth + 'Lectura:')
		self.Identificador.show(depth+1)
		
class Print(Statement):
	def __init__(self,parametros):
		self.parametros = parametros
		
	def show(self, depth):
		print('  '*depth + 'Print')
		self.parametros.show(depth + 1)
#------------------------------------------------------------------
class Expresion(object):
	def __init__(self, hijos):
		self.hijos = hijos
	
	def show(self, depth):
		print('  '*depth + self.name + ':')
		for i in self.hijos:
			self.hijos[i].show(depth+1)
			
class OperacionUnaria(Expresion):
	def __init__(self,p,name):
		self.hijo = p
		self.name = name
		
	def show(self,depth):
		print('  '*depth + self.name + ':')
		self.hijo.show(depth+1)
		
class Agrupadores(Expresion):
	def __init__(self, p, abresimbolo, cierrasimbolo): #( (sa OR p) AND rrdd)
		self.abresimbolo = abresimbolo
		self.cierrasimbolo = cierrasimbolo
		self.expresion = p
		
	def show(self,depth):
		print('  '*depth + self.abresimbolo)
		self.expresion.show(depth+1)
		print('  '*depth + self.cierrasimbolo)
		
class Proyeccion(Expresion):
	def __init__(self,expresion,parametros):
		self.expresion = expresion
		self.parametros = parametros
		
	def show(self, depth):
		#print self.expresion
		self.expresion.show(depth)
		print('  '*(depth+1) + 'Abre Corchetes')
		self.parametros.show(depth+2)
		#print self.parametros
		print('  '*(depth+1) + 'Cierra Corchetes')
		
class OperacionBinaria(Expresion):
	def __init__(self, p,name):
		self.hijos = {'operando izquierdo': p[1], 'operando derecho': p[3]}
		self.name=name
	def show(self, depth):
		print('  '*depth + self.name + ':')
		depth=depth+1
		print ('  '*depth + 'operando izquierdo:'+'  '*depth)
		self.hijos['operando izquierdo'].show(depth+1)
		print ('  '*depth + 'operando derecho:'+'  '*depth)
		self.hijos['operando derecho'].show(depth+1)
	
class Asignar(Expresion):
	def __init__(self,variable,expresion):
		self.hijos = {'variable': variable, 'expresion': expresion}
		self.name = 'Asignacion'
	def show(self, depth):
		print('  '*depth + self.name + ':')
		depth=depth+1
		print ('  '*depth + 'lado izquierdo:'+'  '*depth)
		self.hijos['variable'].show(depth+1)
		print ('  '*depth + 'lado derecho:'+'  '*depth)
		self.hijos['expresion'].show(depth+1)
		
class Asignar_Matriz(Statement):
	def __init__(self,Identificador, proyeccion, expresion):
		self.Identificador = Identificador
		self.proyeccion = proyeccion
		self.expresion = expresion
		
	def show(self,depth):
		print ('  '*depth + 'Asignacion' + ':')
		depth += 1
		print('  '*depth + 'operando izquierdo: ')
		Proyeccion(self.Identificador, self.proyeccion).show(depth +1)
		print('  '*depth + 'operando derecho: ')
		self.expresion.show(depth+1)
		
class Transpuesta(Expresion):
	def __init__(self, valor):
		self.valor = valor
		
	def show(self, depth):
		print ('  '*depth + 'Transpuesta: ')
		self.valor.show(depth+1)
		
#-------------------------------------------------------------------------------------
# LITERALES!
class LiteralNumerico(Expresion):
	def __init__(self,numero):
		self.valor = numero
	def show(self, depth):
		print('  '*depth + 'Literal Numerico:\n'+'  '*(depth+1) + 'valor: '+str(self.valor))
	
class Booleano(Expresion):
	def __init__(self,booleano):
		self.valor = booleano
	def show(self, depth):
		print('  '*depth + 'Booleano:\n'+'  '*(depth+1) + 'valor: '+str(self.valor))
		
class String(Expresion):
	def __init__(self,valor):
		self.valor = valor
		
	def show(self,depth):
		print ('  '*depth + 'String: '+ str(self.valor))

class Declaracion(Statement): 
	def __init__(self,valor,tipo):
		self.tipo = tipo
		self.valor = valor
		
	def show(self, depth):
		print('  '*depth +'Declaracion: ' + str(self.tipo)+'\n'+ '  '*(depth+1) +  'Identificador:\n' + '  '*(depth+2) + 'nombre: '+str(self.valor))

class DeclaracionMatriz(Statement):
	def __init__(self,Identificador,fila,col):
		self.Identificador = Identificador
		self.fila = fila
		self.col = col
	
	def show(self,depth):
		print('  '*depth +'Declaracion: Matriz')
		depth+= 1
		print('  '*depth +'Fila(s):')
		self.fila.show(depth+1)
		print('  '*depth +'Columna(s):')
		self.col.show(depth+1)
		self.Identificador.show(depth)

class ColRow(Statement):
	def __init__(self, Identificador, valor, nombre):
		self.Identificador = Identificador
		self.valor = valor
		self.nombre = nombre
		
	def show(self, depth):
		print ('  '*depth + 'Declaracion: ' + self.nombre)
		print ('  '*(depth+1) + 'Longitud:')
		self.valor.show(depth+2)
		self.Identificador.show(depth+1)

class Variable(Expresion): 
	def __init__(self,valor):
		self.valor = valor
		
	def show(self, depth):
		print('  '*depth + 'Identificador:\n' + '  '*(depth+1) + 'nombre: '+str(self.valor))
#--------------------------------------------------------------------------------------------

def Sintaxer(lx, tokens, textoPrograma):
	error = 0
	precedence = (
		("left", 'OR'),
		("left", 'AND'),
		('right','NOT'),
		("nonassoc","IGUAL2","DISTINTO","MAYORIGUAL","MENORIGUAL","MAYORQUE","MENORQUE"),
		('left', 'MSUMA', 'MMENOS','MAST','MSLASH','MPORCENTAJE', 'MDIV', 'MMOD'),
		('left', 'SUMA', 'MENOS'),
		('left', 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD'),
		('left', 'COMILLASIMPLE'),
		('right', 'UMINUS')
	)
	#def p_comienzo(p):
		#'''comienzo : program
			#| function comienzo'''
		#if len(p) == 2:
			#p[0] = Program(p[1])
		#else:
			#p[0] = Function(p[1])
			
	def p_program(p):
		'''program : PROGRAM statement PUNTOYCOMA END PUNTOYCOMA
			| function program'''
		p[0] = Program(p[2])
	
	#-----------------------------------------------------------------------------------
	### STATEMENTS
	def p_statement_block(p): ## PONER EL IN!
		'statement : USE statement_decl_list IN statement_list END'
		p[0]=Bloque(p[2],p[4])
	
	def p_statement_list(p):
		'''statement_list : statement PUNTOYCOMA
					| statement PUNTOYCOMA statement_list'''
		if len(p)==3:
			p[0]=ListasSt_Dcl(p[1],None)
		else:
			p[0]=ListasSt_Dcl(p[1] ,p[3])
		
	def p_statement_Assing(p):
		'''statement : SET ID IGUAL expression
				| SET ID CORCHETEABRE parametro CORCHETECIERRA IGUAL expression'''
		if len(p)==5:
			p[0] = Asignar(Variable(p[2]),p[4])
		else:
			p[0]=Asignar_Matriz(Variable(p[2]) ,p[4] ,p[7] )
	
	def p_statement_decl_list(p):
		'''statement_decl_list : statement_decl PUNTOYCOMA
							| statement_decl PUNTOYCOMA statement_decl_list'''
		if len(p)==3:
			p[0] = ListasSt_Dcl(p[1],None)
		else:
			p[0] = ListasSt_Dcl(p[1],p[3])
		
	def p_statement_Matrix(p):
		'statement_decl : MATRIX PARENTESISABRE expression COMA expression PARENTESISCIERRA ID'
		p[0] = DeclaracionMatriz(Variable(p[7]),p[3],p[5])
		
	def p_statement_Row(p):
		'statement_decl : ROW PARENTESISABRE expression PARENTESISCIERRA ID'
		p[0] = ColRow(Variable(p[5]),p[3],'Vector Fila')
		
	def p_statement_Col(p):
		'statement_decl : COL PARENTESISABRE expression PARENTESISCIERRA ID'
		p[0] = ColRow(Variable(p[5]),p[3],'Vector Columna')
		
	def p_statement_NUMBER(p):
		'statement_decl : NUMBER ID'
		p[0] = Declaracion(p[2], 'Numerico')
		#if re.match(r'\d+\.d+',p[2]):
			#p[0] = float(p[2])
		#else:
			#p[0]= int(p[2])
			
	def p_statement_BOOLEAN(p):
		'statement_decl : BOOLEAN ID'
		p[0]= Declaracion(p[2], 'Booleano')
		
	def p_statement_READ(p):
		'statement : READ ID'
		p[0] = Read(Variable(p[2]))
		
	def p_statement_PRINT(p):
		'statement : PRINT parametro'
		p[0] = Print(p[2])
		
	def p_function(p):
		'function : FUNCTION ID expression RETURN expression BEGIN statement_list END PUNTOYCOMA'
		p[0] = Function(Variable(p[2]), p[3], p[5],p[7])
# --------------------------------------------------------------------------		
	### EXPRESIONES 
	def p_expression_SUMA(p):
		'expression : expression SUMA expression'
		p[0] = OperacionBinaria(p,'Suma')
	
	def p_expression_AST(p):
		'expression : expression AST expression'
		p[0] = OperacionBinaria(p,'Multiplicacion')
	
	def p_expression_SLASH(p):
		'expression : expression SLASH expression'
		p[0] = OperacionBinaria(p,'Division')
		
	def p_expression_MENOS(p):
		'expression : expression MENOS expression'
		p[0] = OperacionBinaria(p,'Resta')
		
	def p_expression_PORCENTAJE(p):
		'expression : expression PORCENTAJE expression'
		p[0] = OperacionBinaria(p,'Modulo')
		
	def p_expression_DIV(p):
		'expression : expression DIV expression'
		p[0] = OperacionBinaria(p,'Division Entera')
		
	def p_expression_MOD(p):
		'expression : expression MOD expression'
		p[0] = OperacionBinaria(p,'Modulo Entero')

#---------------------------Operaciones Binarias Matrices---------------------------------			
	def p_expression_MSUMA(p):
		'expression : expression MSUMA expression'
		p[0] = OperacionBinaria(p,'Suma Matriz')
	
	def p_expression_MAST(p):
		'expression : expression MAST expression'
		p[0] = OperacionBinaria(p,'Multiplicacion Matriz')
	
	def p_expression_MSLASH(p):
		'expression : expression MSLASH expression'
		p[0] = OperacionBinaria(p,'Division Matriz')
		
	def p_expression_MMENOS(p):
		'expression : expression MMENOS expression'
		p[0] = OperacionBinaria(p,'Resta Matriz')
		
	def p_expression_MPORCENTAJE(p):
		'expression : expression MPORCENTAJE expression'
		p[0] = OperacionBinaria(p,'Modulo Matriz')
		
	def p_expression_MDIV(p):
		'expression : expression MDIV expression'
		p[0] = OperacionBinaria(p,'Division Entera Matriz')
		
	def p_expression_MMOD(p):
		'expression : expression MMOD expression'
		p[0] = OperacionBinaria(p,'Modulo Entero Matriz')
	
	
	##  ## REDUCE ## LITERALES ## ##
	def p_expression_NUMERO(p):
		"expression : NUMERO"
		p[0] = LiteralNumerico(p[1])
		
	def p_expression_ID(p):
		"expression : ID"
		p[0] = Variable(p[1])
			
	def p_expression_BOOLEAN(p):
		"""expression : FALSE
					| TRUE"""
		p[0] = Booleano(p[1])
		
	def p_expression_STRING(p):
		'expression : STRING'
		p[0] = String(p[1])
		
	def p_expression_Comparativos(p):
		"""expression : expression IGUAL2 expression
					| expression DISTINTO expression
					| expression MAYORIGUAL expression
					| expression MENORIGUAL expression
					| expression MAYORQUE expression
					| expression MENORQUE expression"""
		p[0] = OperacionBinaria(p,str(p[2]))
		
	def p_expression_OR(p):
		'expression : expression OR expression'
		p[0] = OperacionBinaria(p,'OR')
	
	def p_expression_AND(p):
		'expression : expression AND expression'
		p[0] = OperacionBinaria(p,'AND')
		
	##########UNARIOS ###########
	def p_menos_unario(p):
		'expression : MENOS expression %prec UMINUS'
		p[0] = OperacionUnaria(p[2],'Menos Unitario')
		
	def p_negacion(p):
		'expression : NOT expression'
		p[0] = OperacionUnaria(p[2],'Negacion')
		
	def p_transpuesta(p):
		'''expression : ID COMILLASIMPLE
			| LLAVESABRE parametro_matriz LLAVESCIERRA COMILLASIMPLE'''
		if len(p)==3:
			p[0] = Transpuesta(Variable(p[1]))
		else:
			p[0] = Transpuesta(p[2])
	#--------------------------------------------------------------
	def p_parentesis(p):
		'expression : PARENTESISABRE parametro PARENTESISCIERRA'
		p[0] = Agrupadores(p[2],'Abre Parentesis','Cierra Parentesis')
		
	def p_parametros(p):
		"""parametro : expression
					| expression COMA parametro"""
		if len(p)==2:
			p[0] = ListasSt_Dcl(p[1],None)
		else:
			p[0] = ListasSt_Dcl(p[1],p[3])
	#------------------------------------------------------------------
	def p_llaves(p):
		'expression : LLAVESABRE parametro_matriz LLAVESCIERRA'	
		p[0] = Agrupadores(p[2],'Abre Llaves','Cierra Llaves')	
	
	def p_parametros_matriz(p):
		"""parametro_matriz : parametro
					| parametro DOSPUNTOS parametro_matriz"""
		if len(p)==2:
			p[0] = ListasSt_Dcl(p[1],None)
		else:
			p[0] = ListasSt_Dcl(p[1],p[3])
	#-----------------------------------------------------------------------
	def p_proyeccion(p):
		'expression : expression CORCHETEABRE parametro CORCHETECIERRA'
		p[0] = Proyeccion(p[1],p[3])
		
	# instrucciones condicionales
	def p_IF(p):
		'''statement : IF expression THEN statement_list ELSE statement_list END
					| IF expression THEN statement END'''
		if len(p) == 8:
			p[0] = instruccion_IF(p[2],p[4],p[6])
		else:
			p[0] = instruccion_IF(p[2],p[4],None)
	
	def p_FOR(p):
		'statement : FOR ID IN expression DO statement_list END'
		p[0] = instruccion_FOR(Variable(p[2]),p[4],p[6])
		
	def p_WHILE(p):
		'statement : WHILE expression DO statement_list END'
		p[0] = instruccion_WHILE(p[2], p[4])
		
	def p_error(p):
		if p==None:
			print ("Error Sintactico, estructura incompleta")
		else:
			print ("Error: {} de tipo {} encontrado en la fila {}, columna {}".format(p.value,p.type,p.lineno,p.lexpos))
		error = 1
		sys.exit(error)
		
	yacc.yacc(start='program')	
	yacc.parse(lexer=lx).show(0)
	return error
