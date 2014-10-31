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
	def __init__(self,Identificador, parametros, tipo, instrucciones,siguiente):
		self.Identificador = Identificador
		self.parametros = parametros
		self.tipo = tipo
		self.instrucciones = instrucciones
		self.siguiente= siguiente
		
	def show(self, depth):
		print('  '*depth + 'FUNCTION:')
		self.Identificador.show(depth+1)
		print('  '*(depth+1) + 'Parametros:')
		self.parametros.show(depth+2)
		print('  '*(depth+1) + 'Retorna Tipo:')
		print('  '*(depth+2) + self.tipo)
		print('  '*(depth+1) + 'BEGIN:')
		self.instrucciones.show(depth+2)
		print('  '*(depth+1) + 'END\n')
		self.siguiente.show(depth)
		
class Program:
	def __init__(self,cuerpo):
		self.cuerpo=cuerpo

	def show(self, depth):
		print 'PROGRAM'
		self.cuerpo.show(depth+1)
		print 'END'
		
class Statement:
	pass

class ListasSt(Statement):
	def __init__(self, AnStatement, ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		
	def show(self, depth):
		if self.ManyStatements == None:
			self.AnStatement.show(depth)
		else:
			self.AnStatement.show(depth)
			self.ManyStatements.show(depth)
			
	def check(self, tabla):
		if self.ManyStatements == None:
			self.AnStatement.check(tabla)
		else:
			self.AnStatement.check(tabla)
			self.ManyStatements.check(tabla)
			
class ListasSt_Dcl(Statement):
	def __init__(self, AnStatement, ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		self.IdValor = {}
		self.Aux = {}
		self.clave = None
		
	def show(self, depth):
		if self.ManyStatements == None:
			self.AnStatement.show(depth)
		else:
			self.AnStatement.show(depth)
			self.ManyStatements.show(depth)
		
	def getDict(self):
		self.clave =self.AnStatement.getValor()
		self.IdValor[self.clave]=self.AnStatement.getTipo()
		if self.ManyStatements != None:
			self.Aux = self.ManyStatements.getDict()
			for i in self.Aux:
				if self.clave != i:
					self.IdValor[i]=self.Aux[i]
				else:
					print('Error de contexto: variable {} ya declarada'.format(i))
					exit(3)
		return self.IdValor

class Bloque(Statement):
	def __init__(self,declaraciones,instrucciones):
		self.declaraciones=declaraciones
		self.instrucciones=instrucciones
		self.diccionario={}
		
		
	def show(self,depth):
		print('  '*depth+'USE:')
		self.declaraciones.show(depth+1)
		self.diccionario=self.declaraciones.getDict();
		print(self.diccionario)
		
############ LLAMAR A ALCANCE  ############
		print('  '*depth+'IN:')
		scope = Alcance(self.diccionario,None)
		self.instrucciones.check(scope)
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
		print('  '*depth + 'THEN:')
		self.instrucciones.show(depth+1)
		if self.instruccionesElse != None:
			print('  '*depth + 'ELSE:')
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
		print('  '*depth + 'IN:')
		self.estructura.show(depth+1)
		print('  '*depth + 'DO:')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
class instruccion_WHILE(Statement):
	def __init__(self, condicion,instrucciones):
		self.condicion = condicion
		self.instrucciones = instrucciones
		
	def show(self, depth):
		print('  '*depth+'WHILE:')
		self.condicion.show(depth+1)
		print('  '*depth + 'DO:')
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
		print('  '*depth + 'Print:')
		self.parametros.show(depth + 1)
		
class Return(Statement):
	def __init__(self,statement):
		self.statement = statement
		
	def show(self, depth):
		print('  '*depth + 'Return:')
		self.statement.show(depth + 1)
		
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
	def __init__(self, p, abresimbolo, cierrasimbolo):
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
		
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		print operandoder
		return self.equals(operandoizq,operandoder,self.name)
	
	# SUMA RESTA MULT
	def equals(self,izq,der,operador):
		if (isinstance(izq,TNum) and isinstance(der,TNum)):
			return izq
		### HAY OPERADORES BINARIOS QUE RETORNAN BOOLEANOS  ><##
		### FALTA VERIFICACION DE MATRIZ ###
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(6)

class OperacionBinariaSRM(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		print operandoder
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(self,izq,der,operador):
		if (isinstance(izq,TNum) and isinstance(der,TNum)):
			return izq
		elif (isinstance(izq,TMatrix) and isinstance(der,TMatrix)):
			if (operador=='Suma' or operador=='Resta'):
				if (izq.TamFila==der.TamFila and izq.TamColumna==der.TamColumna):
					return izq
				else:
					print ("Error: dimensiones de matrices incorrectas, no pueden ser operadas con el operador {} ".format(operador))
					exit(6)
			else:#Multiplicacion
				if (izq.TamColumna==der.TamFila):
					return TMatrix(izq.TamFila,der.TamColumna)
				else:
					print ("Error: dimensiones de matrices incorrectas, no pueden ser operadas con el operador {} ".format(operador))
					exit(6)
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(6)
			
class OperacionBinariaComp(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		print operandoder
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(self,izq,der,operador):
		if izq == der:
			return izq
		### HAY OPERADORES BINARIOS QUE RETORNAN BOOLEANOS  ><##
		### FALTA VERIFICACION DE MATRIZ ###
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
		exit(6)
	
class OperacionBinariaIgualdad(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		print operandoder
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(izq,der,operador):
		if izq == der:### FALTA VERIFICACION DE MATRIZ ###
			return izq
		### HAY OPERADORES BINARIOS QUE RETORNAN BOOLEANOS  ><##
		### FALTA VERIFICACION DE MATRIZ ###
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(6)
		
class OperacionBinariaOpBool(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		print operandoder
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(izq,der,operador):
		if izq == der:
			return izq
		###  OPERADORES BINARIOS QUE RETORNAN BOOLEANOS  ><##
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
		exit(6)
		
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
		
	def check(self,tabla):
		ladoizq = self.hijos['variable'].check(tabla)
		ladoder = self.hijos['expresion'].check(tabla)
		return self.equals(ladoizq,ladoder)
		
	def equals(self,izq,der):
		if isinstance(izq,der.__class__):
			if izq.__class__.__name__=='TMatrix':
				if (izq.TamFila==der.TamFila and der.TamColumna==izq.TamColumna):
					return izq
				else:
					print ("Error: Asignacion Invalida, dimensiones de matrices incorrectas")
					exit(7)
			return izq
		else:
			print ("Error: Asignacion Invalida, esperado tipo '{}' y encontrado tipo '{}' ".format(izq.tipo,der.tipo))
			exit(7)
		
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
		
	def check(self,tabla):
		pass
		#ladoizq = self.
		
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
		
	def check(self,tabla):
		return TNum(self.valor)
	
class Booleano(Expresion):
	def __init__(self,booleano):
		self.valor = booleano
	def show(self, depth):
		print('  '*depth + 'Booleano:\n'+'  '*(depth+1) + 'valor: '+str(self.valor))
	def check(self,tabla):
		return TBool(self.valor)
		
class String(Expresion):
	def __init__(self,valor):
		self.valor = valor
		
	def show(self,depth):
		print ('  '*depth + 'String: '+ str(self.valor))

class Declaracion(Statement): 
	def __init__(self,nombre,tipo,expresion):
		self.tipo = tipo
		self.nombre = nombre
		self.expresion = expresion
		
	def show(self, depth):
		print('  '*depth +'Declaracion: '+str(self.tipo))
		if self.expresion!=None:
			Asignar(self.nombre, self.expresion).show(depth+1)
		else:
			print('  '*(depth+1)+'Identificador:')
			self.nombre.show(depth+2)
		
	def getTipo(self):
		for i in Tipo.__subclasses__():
			if i.tipo==self.tipo:
				return i(self.nombre)
	def getValor(self):
		return self.nombre.valor

class DeclaracionMatriz(Statement):
	def __init__(self,Identificador,fila,col,expresion):
		self.Identificador = Identificador
		self.fila = fila
		self.col = col
		self.expresion = expresion
	
	def show(self,depth):
		print('  '*depth +'Declaracion: Matriz')
		depth+= 1
		print('  '*depth +'Fila(s):')
		self.fila.show(depth+1)
		print('  '*depth +'Columna(s):')
		self.col.show(depth+1)
		self.check()
		if self.expresion!=None:
			Asignar(self.Identificador,self.expresion).show(depth)
		else:
			self.Identificador.show(depth)
			
	def getTipo(self):
		return TMatrix(self.fila.valor,self.col.valor)
	def getValor(self):
		return self.Identificador.valor
	
	def check(self):
		# Verificacion que dentro de los parentesis esten enteros
		if  (isinstance(self.fila,LiteralNumerico) and isinstance(self.col,LiteralNumerico)):
			if self.expresion != None:
				print self.expresion
		else:
			print('Error: invalida declaracion de matriz, esperado tipo Numerico ')
			exit(7)
			
	############ VERIFICAR QUE DENTRO DE LOS PARENTESIS ESTEN SON ENTEROS!! ##########

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
		
	def check(self,tabla):
		return tabla.buscar(self.valor)
	
class Tipo(object):
	pass
	
class TNum(Tipo):
	tipo = 'Numerico'
	def __init__(self,valor):
		self.valor = valor
		
	
class TBool(Tipo):
	tipo='Booleano'
	def __init__(self,valor):
		self.valor = valor
	
class TMatrix(Tipo):
	def __init__(self,TamFila,TamColumna):
		self.TamFila=TamFila
		self.TamColumna=TamColumna
		self.tipo = 'Matriz'

class Alcance: #decls se crea al ver un USE o un FOR
	def __init__ (self,decls,padre):
		self.locales={}
		for key in decls: 
			self.locales[key]=decls[key]
		self.padre=padre
		self.hijos=[]
		if self.padre != None:
			self.padre.hijos.append(self)
	
	def buscar(self, nombre):
		if nombre in self.locales:
			return self.locales[nombre]
		elif self.padre != None:
			return self.padre.buscar(nombre)
		else:
			print('Error de contexto: variable {} no declarada'.format(nombre))
			exit(4)

#--------------------------------------------------------------------------------------------

def Sintaxer(lx, tokens, textoPrograma):
	error = 0
	precedence = (
		("left", 'OR'),
		("left", 'AND'),
		("nonassoc","IGUAL2","DISTINTO","MAYORIGUAL","MENORIGUAL","MAYORQUE","MENORQUE"),
		('right','NOT'), 
		('left', 'MSUMA', 'MMENOS','MAST','MSLASH','MPORCENTAJE', 'MDIV', 'MMOD'),
		('left', 'SUMA', 'MENOS'),
		('left', 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD'),
		('left', 'COMILLASIMPLE'),
		('right', 'UMINUS')
	)
	
	def p_program(p):
		'''program : PROGRAM statement_list END PUNTOYCOMA
			| FUNCTION ID PARENTESISABRE statement_decl_param PARENTESISCIERRA RETURN type BEGIN function_statement_list END PUNTOYCOMA program'''
		if len(p)==5:
			p[0] = Program(p[2])
		else:
			p[0] = Function(Variable(p[2]), p[4], p[7],p[9],p[12])
			
	#-----------------------------------------------------------------------------------
	### FUNCTION statements
	
	#def p_function_list(p):
		#'''function_list : FUNCTION ID PARENTESISABRE statement_decl_param PARENTESISCIERRA RETURN type BEGIN function_statement_list END PUNTOYCOMA
					#| FUNCTION ID PARENTESISABRE statement_decl_param PARENTESISCIERRA RETURN type BEGIN function_statement_list END PUNTOYCOMA function_list'''
		#if len(p)==12:
			#p[0] = Function(Variable(p[2]), p[4], p[7],p[9],None)
		#else:
			#p[0] = Function(Variable(p[2]), p[4], p[7],p[9],p[12])
	
	def p_function_statement_list(p):
		'''function_statement_list : function_statement PUNTOYCOMA
					| function_statement PUNTOYCOMA function_statement_list'''
		if len(p)==3:
			p[0]=ListasSt_Dcl(p[1],None)
		else:
			p[0]=ListasSt_Dcl(p[1] ,p[3])
	
	def p_function_RETURN(p):
		'function_statement : RETURN expression'
		p[0] = Return(p[2])
	
	def p_function_statement_READ(p):
		'function_statement : READ ID'
		p[0] = Read(Variable(p[2]))
		
	def p_function_statement_PRINT(p):
		'function_statement : PRINT parametro'
		p[0] = Print(p[2])
		
	def p_function_statement_Assing(p):
		'''function_statement : SET ID IGUAL expression
				| SET ID CORCHETEABRE parametro CORCHETECIERRA IGUAL expression'''
		if len(p)==5:
			p[0] = Asignar(Variable(p[2]),p[4])
		else:
			p[0] = Asignar_Matriz(Variable(p[2]) ,p[4] ,p[7] )
	
	# instrucciones de control
	def p_function_IF(p):
		'''function_statement : IF expression THEN function_statement_list ELSE function_statement_list END
					| IF expression THEN function_statement_list END'''
		if len(p) == 8:
			p[0] = instruccion_IF(p[2],p[4],p[6])
		else:
			p[0] = instruccion_IF(p[2],p[4],None)
	
	def p_fuction_FOR(p):
		'function_statement : FOR ID IN expression DO function_statement_list END'
		p[0] = instruccion_FOR(Variable(p[2]),p[4],p[6])
		
	def p_function_WHILE(p):
		'function_statement : WHILE expression DO function_statement_list END'
		p[0] = instruccion_WHILE(p[2], p[4])
	
	#-----------------------------------------------------------------------------------
	### STATEMENTS
	def p_statement_block(p):
		'statement : USE statement_decl_list IN statement_list END'
		p[0]=Bloque(p[2],p[4])
	
	def p_statement_list(p):
		'''statement_list : statement PUNTOYCOMA
					| statement PUNTOYCOMA statement_list'''
		if len(p)==3:
			p[0]=ListasSt(p[1],None)
		else:
			p[0]=ListasSt(p[1] ,p[3])
	
	def p_statement_decl_param(p):
		'''statement_decl_param : statement_decl
							| statement_decl COMA statement_decl_param'''
		if len(p)==2:
			p[0] = ListasSt_Dcl(p[1],None)
		else:
			p[0] = ListasSt_Dcl(p[1],p[3])
	
	def p_statement_decl_list(p):
		'''statement_decl_list : statement_decl PUNTOYCOMA
							| statement_decl PUNTOYCOMA statement_decl_list'''
		if len(p)==3:
			p[0] = ListasSt_Dcl(p[1],None)
		else:
			p[0] = ListasSt_Dcl(p[1],p[3])
		
	def p_statement_Matrix(p):
		'''statement_decl : MATRIX PARENTESISABRE expression COMA expression PARENTESISCIERRA ID
							| MATRIX PARENTESISABRE expression COMA expression PARENTESISCIERRA ID IGUAL expression'''
		if len(p)==8:
			p[0] = DeclaracionMatriz(Variable(p[7]),p[3],p[5],None)
		else:
			p[0] = DeclaracionMatriz(Variable(p[7]),p[3],p[5],p[9])
		
	def p_statement_Row(p):
		'statement_decl : ROW PARENTESISABRE expression PARENTESISCIERRA ID'
		p[0] = ColRow(Variable(p[5]),p[3],'Vector Fila')
		
	def p_statement_Col(p):
		'statement_decl : COL PARENTESISABRE expression PARENTESISCIERRA ID'
		p[0] = ColRow(Variable(p[5]),p[3],'Vector Columna')
		
	def p_statement_NUMBER(p):
		'''statement_decl : NUMBER ID
						| NUMBER ID IGUAL expression'''
		if len(p)==3:
			p[0] = Declaracion(Variable(p[2]), 'Numerico',None)
		else:
			p[0] = Declaracion(Variable(p[2]), 'Numerico',p[4])
			
	def p_statement_BOOLEAN(p):
		'statement_decl : BOOLEAN ID'
		p[0]= Declaracion(Variable(p[2]), 'Booleano')
		
	def p_statement_READ(p):
		'statement : READ ID'
		p[0] = Read(Variable(p[2]))
		
	def p_statement_PRINT(p):
		'statement : PRINT parametro'
		p[0] = Print(p[2])
		
	def p_statement_Assing(p):
		'''statement : SET ID IGUAL expression
				| SET ID CORCHETEABRE parametro CORCHETECIERRA IGUAL expression'''
		if len(p)==5:
			p[0] = Asignar(Variable(p[2]),p[4])
		else:
			p[0]=Asignar_Matriz(Variable(p[2]) ,p[4] ,p[7] )
	
	# instrucciones de control
	def p_IF(p):
		'''statement : IF expression THEN statement_list ELSE statement_list END
					| IF expression THEN statement_list END'''
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
	
# --------------------------------------------------------------------------
	### AUXILIAR 
	def p_type(p):
		'''type : NUMBER
				| BOOLEAN
				| MATRIX PARENTESISABRE expression COMA expression PARENTESISCIERRA
				| ROW PARENTESISABRE expression PARENTESISCIERRA
				| COL PARENTESISABRE expression PARENTESISCIERRA'''
		p[0] = p[1]
		
# --------------------------------------------------------------------------
	### EXPRESIONES 

#-------------- Numericas y Matriciales ------------------------------	
	def p_expression_SUMA(p):
		'expression : expression SUMA expression'
		p[0] = OperacionBinariaSRM(p,'Suma')
	
	def p_expression_AST(p):
		'expression : expression AST expression'
		p[0] = OperacionBinariaSRM(p,'Multiplicacion')
	
	def p_expression_MENOS(p):
		'expression : expression MENOS expression'
		p[0] = OperacionBinariaSRM(p,'Resta')
		
#-------------------- Numericas -------------------------------------------
	def p_expression_SLASH(p):
		'expression : expression SLASH expression'
		p[0] = OperacionBinaria(p,'Division')
		
	def p_expression_PORCENTAJE(p):
		'expression : expression PORCENTAJE expression'
		p[0] = OperacionBinaria(p,'Modulo')
		
	def p_expression_DIV(p):
		'expression : expression DIV expression'
		p[0] = OperacionBinaria(p,'Division Entera')
		
	def p_expression_MOD(p):
		'expression : expression MOD expression'
		p[0] = OperacionBinaria(p,'Modulo Entero')

#---------------------------Operaciones Binarias Cruzadas---------------------------------			
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
		'string : STRING'
		p[0] = String(p[1])
		
	def p_expression_Comparativos(p):
		"""expression : expression MAYORIGUAL expression
					| expression MENORIGUAL expression
					| expression MAYORQUE expression
					| expression MENORQUE expression"""
		p[0] = OperacionBinariaComp(p,str(p[2]))
		
	def p_expression_Comparativos_Igualdad(p):
		"""expression : expression IGUAL2 expression
					| expression DISTINTO expression"""
		p[0] = OperacionBinariaIgualdad(p,str(p[2]))
		
	def p_expression_OR(p):
		'expression : expression OR expression'
		p[0] = OperacionBinariaOpBool(p,'OR')
	
	def p_expression_AND(p):
		'expression : expression AND expression'
		p[0] = OperacionBinariaOpBool(p,'AND')
		
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
		'expression : PARENTESISABRE expression PARENTESISCIERRA'
		p[0] = Agrupadores(p[2],'Abre Parentesis','Cierra Parentesis')
	
	#def p_parametros(p):
		#'parametros : PARENTESISABRE parametro PARENTESISCIERRA'
		#p[0] = Agrupadores(p[2],'Abre Parentesis','Cierra Parentesis')
		
	def p_parametro(p):
		"""parametro : expression
					| string
					| expression COMA parametro
					| string COMA parametro"""
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
		
	def p_error(p):
		if p==None:
			print ("Error Sintactico, estructura incompleta")
		else:
			print ("Error: {} de tipo {} encontrado en la fila {}, columna {}".format(p.value,p.type,p.lineno,p.lexpos))
		error = 2
		exit(error)
		
	yacc.yacc(start='program')
	yacc.parse(lexer=lx).show(0)
	return (error)
