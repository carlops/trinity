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
		
class Bloque(Statement):
	def __init__(self,declaraciones,instrucciones):
		self.declaraciones=declaraciones
		self.instrucciones=instrucciones
		self.diccionario={}
		self.diccionario=self.declaraciones.getDict();
		#print(self.diccionario)
		
	def show(self,depth): ## este show hay que cambiarlo por check
		print('  '*depth+'USE:')
		self.declaraciones.show(depth+1)
		print('  '*depth+'IN:')
		self.instrucciones.show(depth+1)
		print('  '*depth+'END')
		scope = Alcance('main',self.diccionario,None,0)
		self.declaraciones.check(scope)
		self.instrucciones.check(scope)
		scope.Mostrar()
		#self.check(self.scope)
		
	def check(self,tabla):
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
			
class ParametrosProyeccion(ListasSt):
	def check(self, tabla):
		primer=self.AnStatement.check(tabla)
		if not isinstance(primer,TNum):
			print('Error: proyeccion matricial, esperado tipo \'Numerico\' y recibido tipo {}'.format(primer.__class__.__name__))
			exit(10)
		#if int(primer.getValor())<1:
			#print('Error: proyeccion matricial, los indices deben ser mayores que uno')
			#exit(10)
		#valores=[int(primer.getValor())]
		if self.ManyStatements != None:
			segundo=self.ManyStatements.check(tabla)
			#valores.append(int(segundo.getValor()))
			if not isinstance(segundo,TNum):
				print('Error: proyeccion matricial, esperado tipo \'Numerico\' y recibido tipo {}'.format(segundo.__class__.__name__))
				exit(10)
			#if int(segundo.getValor())<1:
				#print('Error: proyeccion matricial, los indices deben ser mayores que uno')
				#exit(10)
		#return valores
		
class ParametrosMatriz(Statement):
	def __init__(self, UnParametro, OtrosParametros):
		self.UnParametro = UnParametro
		self.OtrosParametros = OtrosParametros
		
	def show(self, depth):
		if self.OtrosParametros == None:
			self.UnParametro.show(depth)
		else:
			self.UnParametro.show(depth)
			self.OtrosParametros.show(depth)
			
	def check(self, tabla):
		if self.OtrosParametros == None:
			tipo = self.UnParametro.check(tabla)
			if not isinstance(tipo,TNum):
				print("Error: parametro invalido en matriz encontrado tipo '{}' esperado tipo 'Numerico'".format(tipo))
				exit(8)
		else:
			tipo = self.UnParametro.check(tabla)
			if isinstance(tipo,TNum):
				self.OtrosParametros.check(tabla)
			else:
				print("Error: parametro invalido en matriz encontrado tipo '{}' esperado tipo 'Numerico'".format(tipo))
				exit(8)
		return self.size()
		
	def size(self):
		if self.OtrosParametros == None:
			return 1
		else:
			return 1 + self.OtrosParametros.size()
		
class ListasSt_Dcl(Statement):
	def __init__(self, AnStatement, ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		self.IdValor = {}
		self.Aux = {}
		self.clave = None
		
	def show(self, depth):
		self.AnStatement.show(depth)
		if self.ManyStatements != None:
			self.ManyStatements.show(depth)
			
	def check(self, tabla):
		self.AnStatement.check(tabla)
		if self.ManyStatements != None:
			self.ManyStatements.check(tabla)
			
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
	
class LiteralMatricial(Statement):
	def __init__(self, parametroActual, restoParametros):
		self.parametroActual = parametroActual
		self.restoParametros = restoParametros
		self.NumFilas=1
		self.NumCol=0
		
	def show(self, depth):
		if self.restoParametros == None:
			self.parametroActual.show(depth)
		else:
			self.parametroActual.show(depth)
			print(" "*(depth+4) + "DOSPUNTOS")
			self.restoParametros.show(depth)
		
	def check(self,tabla): ######### CAMBIAR #########
		self.NumCol= self.parametroActual.check(tabla)
		self.NumFilas = self.checkMatriz(1,self.NumCol,tabla)
		filas = str(self.NumFilas)
		columnas = str(self.NumCol)
		return TMatrix(filas,columnas)

	def checkMatriz(self,filas,columnas,tabla):
		if columnas!= self.parametroActual.check(tabla):
			print("Error en Literal Matricial: las columnas deben tener la misma longitud")
			exit(9)
		if self.restoParametros != None:
			#col=col+ self.parametroActual.check(tabla)
			filas = filas + self.restoParametros.checkMatriz(filas,columnas,tabla)
		return filas
		
		
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
		
	def check(self, tabla):
		tipo=self.hijo.check(tabla)
		if self.name=='Negacion':
			if not isinstance(tipo,TBool):
				print ("Error: esperado tipo Booleano, encontrado "+tipo)
				exit(13)
		else:
			if not isinstance(tipo,TNum):
				print ("Error: esperado tipo Numerico, encontrado "+tipo)
				exit(13)
		return tipo
		
class Agrupadores(Expresion):
	def __init__(self, expresion, abresimbolo, cierrasimbolo):
		self.abresimbolo = abresimbolo
		self.cierrasimbolo = cierrasimbolo
		self.expresion = expresion
		
	def show(self,depth):
		print('  '*depth + self.abresimbolo)
		self.expresion.show(depth+1)
		print('  '*depth + self.cierrasimbolo)
		
	def check(self,tabla):
		return self.expresion.check(tabla)
	
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
		#print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		#print operandoder
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

class OperacionBinariaCruzada(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		operandoder = self.hijos['operando derecho'].check(tabla)
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(self,izq,der,operador):
		if (isinstance(izq,TNum) and isinstance(der,TMatrix)):
			return der
		elif (isinstance(izq,TMatrix) and isinstance(der,TNum)):
			return izq
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(15)

class OperacionBinariaSRM(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		#print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		#print operandoder
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
		#print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		#print operandoder
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
		#print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		#print operandoder
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
		#print operandoizq
		operandoder = self.hijos['operando derecho'].check(tabla)
		#print operandoder
		if not isinstance(operandoizq,TBool):
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(12)
		if not isinstance(operandoder,TBool):
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq,der,operador))
			exit(12)
		return operandoizq
		
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
			
		
class Asignar_Matriz_Elem(Statement):
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
		ladoIzq = self.Identificador.check(tabla)
		if not isinstance(ladoIzq,TMatrix):
			print('Error: Esperado tipo matriz y encontrado '+ ladoIzq.tipo)
		self.proyeccion.check(tabla)#Verifica que sean numericos
		#error=False
		#print parametros
		#fila=int(ladoIzq.getTamFila())
		#col =int(ladoIzq.getTamCol())
		#if len(parametros)==1:
			#if col==1 and fila<parametros[0]:
				#error=True
			#elif fila==1 and col<parametros[0]:
				#error=True
			#else:
				#error=True
		#elif len(parametros)==2:
			#print "Caso 2"
			#if fila<parametros[0] or col<parametros[1]:
				#error=True
		#if error:
			#print('Error: Proyeccion no esta dentro del rango definido para la matriz')
			#exit(10)
		ladoDer = self.expresion.check(tabla)
		if not isinstance(ladoDer,TNum):
			print('Error: Esperado tipo numerico y encontrado '+ ladoDer.tipo)
			exit(10)
		
class Transpuesta(Expresion):
	def __init__(self, valor):
		self.valor = valor
		
	def show(self, depth):
		print ('  '*depth + 'Transpuesta: ')
		self.valor.show(depth+1)
		
	def check(self,tabla):
		tipo=self.valor.check(tabla)
		if not isinstance(tipo,TMatrix):
			print("Error: Transpuesta, esperado tipo Matriz, encontrado "+tipo.tipo)
			exit(14)
		return tipo
		
		
#-------------------------------------------------------------------------------------
# LITERALES!
class LiteralNumerico(Expresion):
	def __init__(self,numero):
		self.valor = numero
	def show(self, depth):
		print('  '*depth + 'Literal Numerico:\n'+'  '*(depth+1) + 'valor: '+str(self.valor))
	def check(self,tabla):
		return TNum(self.valor)
	def getValor(self):
		return self.valor
	
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
		
	def check(self,tabla):
		if self.expresion!=None:
			if (self.expresion.check(tabla).getTipo()!=self.tipo):
				print ('Error: Declaracion invalida, declarado tipo \'{}\', encontrado tipo \'{}\''.format(self.tipo,self.expresion.check(tabla).getTipo()))
				exit(8)
		return self.tipo
	
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
		if self.expresion!=None:
			Asignar(self.Identificador,self.expresion).show(depth)
		else:
			self.Identificador.show(depth)
		
	def getTipo(self):
		return TMatrix(self.fila.valor,self.col.valor)
	
	def getValor(self):
		return self.Identificador.valor
	
	def check(self,tabla):
		# Verificacion que dentro de los parentesis esten enteros
		if  (isinstance(self.fila,LiteralNumerico) and isinstance(self.col,LiteralNumerico)):
			if '.' in (self.fila.check(tabla).getValor()):
				print('Error: invalida declaracion de matriz, esperado tipo Entero')
				exit(7)
			else:
				if int(self.fila.check(tabla).getValor()) <1:
					print('Error: invalida declaracion de matriz, la cantidad de filas debe ser positiva')
					exit(7)
			if '.' in (self.col.check(tabla).getValor()):
				print('Error: invalida declaracion de matriz, esperado tipo Entero')
				exit(7)
			else:
				if int(self.col.check(tabla).getValor()) <1:
					print('Error: invalida declaracion de matriz, la cantidad de columnas debe ser positiva')
					exit(7)
			
			if self.expresion != None:
				Asignar(self.Identificador,self.expresion).check(tabla)
		else:
			print('Error: invalida declaracion de matriz, esperado tipo Numerico ')
			exit(7)
			
	############ VERIFICAR QUE DENTRO DE LOS PARENTESIS ESTEN SON ENTEROS!! ##########

class ColRow(Statement):
	def __init__(self, Identificador, valor, nombre,expresion):
		self.Identificador = Identificador
		self.valor = valor
		self.nombre = nombre
		self.expresion = expresion
		self.fila=LiteralNumerico('1')
		self.col=LiteralNumerico('1')
		
	def show(self, depth):
		print ('  '*depth + 'Declaracion: ' + self.nombre)
		print ('  '*(depth+1) + 'Longitud:')
		self.valor.show(depth+2)
		self.Identificador.show(depth+1)
		if self.expresion!=None:
			Asignar(self.Identificador,self.expresion).show(depth)
		
	def check(self,tabla):
		tipo = self.valor.check(tabla)
		if not isinstance(tipo,TNum):
			print ('Error: declaracion de vector invalida, esperado tipo \'Numerico\' encontrado tipo \'{}\''.format(tipo.tipo))
			exit(11)
		DeclaracionMatriz(self.Identificador,self.fila,self.col,self.expresion).check(tabla)
		
	def getValor(self):
		return self.Identificador.valor
	
	def getTipo(self):
		if self.nombre=='Vector Columna':
			self.fila=self.valor
		elif self.nombre=='Vector Fila':
			self.col=self.valor
		return TMatrix(self.fila.valor,self.col.valor)

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
	def getValor(self):
		return self.valor
	def getTipo(self):
		return self.tipo
	def toStr(self):
		return self.tipo
		
class TBool(Tipo):
	tipo='Booleano'
	def __init__(self,valor):
		self.valor = valor
	def getValor(self):
		return self.valor
	def getTipo(self):
		return self.tipo
	def toStr(self):
		return self.tipo
	
class TMatrix(Tipo):
	tipo = 'Matriz'
	def __init__(self,TamFila,TamColumna):
		self.TamFila=TamFila
		self.TamColumna=TamColumna
	def getTamFila(self):
		#return self.TamFila.getValor()
		return self.TamFila
	def getTamCol(self):
		#return self.TamColumna.getValor()
		return self.TamColumna
	def getTipo(self):
		return self.tipo
	def toStr(self):
		return '{}({},{})'.format(self.tipo,self.TamFila,self.TamColumna)

class Alcance: #decls se crea al ver un USE o un FOR
	def __init__ (self,nombre,decls,padre,nivel):
		self.nombre = nombre
		self.nivel = nivel
		self.locales={}
		for key in decls: 
			self.locales[key]=decls[key]
		self.padre=padre
		self.hijos=[]
		if self.padre != None:
			self.padre.hijos.append(self)
			
	def Mostrar(self):
		depth=' '*self.nivel
		print(depth+'Alcance '+self.nombre +':')
		depth=' '*(self.nivel+2)
		print(depth+'Simbolos:')
		depth=' '*(self.nivel+4)
		for i in self.locales.items():
			print(depth+str(i[0])+': '+i[1].toStr())
		depth=' '*(self.nivel+2)
		if self.hijos==[]:
			print(depth+'Hijos: []')
		else:
			print(depth+'Hijos:')
			for i in self.hijos:
				i.Mostrar()
	
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
			p[0] = Asignar_Matriz_Elem(Variable(p[2]) ,p[4] ,p[7] )
	
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
	
	def p_statement_expresion(p):
		'statement : expression'
		p[0]=p[1]
	
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
		'''statement_decl : ROW PARENTESISABRE expression PARENTESISCIERRA ID
						| ROW PARENTESISABRE expression PARENTESISCIERRA ID IGUAL expression'''
		if len(p)==6:
			p[0] = ColRow(Variable(p[5]),p[3],'Vector Fila',None)
		else:
			p[0] = ColRow(Variable(p[5]),p[3],'Vector Fila',p[7])
			
	def p_statement_Col(p):
		'''statement_decl : COL PARENTESISABRE expression PARENTESISCIERRA ID
						| COL PARENTESISABRE expression PARENTESISCIERRA ID IGUAL expression'''
		if len(p)==6:
			p[0] = ColRow(Variable(p[5]),p[3],'Vector Columna',None)
		else:
			p[0] = ColRow(Variable(p[5]),p[3],'Vector Columna',p[7])
	def p_statement_NUMBER(p):
		'''statement_decl : NUMBER ID
						| NUMBER ID IGUAL expression'''
		if len(p)==3:
			p[0] = Declaracion(Variable(p[2]), 'Numerico',None)
		else:
			p[0] = Declaracion(Variable(p[2]), 'Numerico',p[4])
			
	def p_statement_BOOLEAN(p):
		'''statement_decl : BOOLEAN ID
						| BOOLEAN ID IGUAL expression'''
		if len(p)==3:
			p[0]= Declaracion(Variable(p[2]), 'Booleano',None)
		else:
			p[0]= Declaracion(Variable(p[2]), 'Booleano',p[4])
			
	def p_statement_READ(p):
		'statement : READ ID'
		p[0] = Read(Variable(p[2]))
		
	def p_statement_PRINT(p):
		'statement : PRINT parametros_impresion'
		p[0] = Print(p[2])
		
	def p_statement_Assing(p):
		'''statement : SET ID IGUAL expression
				| SET ID CORCHETEABRE parametro_proyeccion CORCHETECIERRA IGUAL expression'''
		if len(p)==5:
			p[0] = Asignar(Variable(p[2]),p[4])
		else:
			p[0]=Asignar_Matriz_Elem(Variable(p[2]) ,p[4] ,p[7] )
	
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
		p[0] = OperacionBinariaCruzada(p,'Suma Matriz')
	
	def p_expression_MAST(p):
		'expression : expression MAST expression'
		p[0] = OperacionBinariaCruzada(p,'Multiplicacion Matriz')
	
	def p_expression_MSLASH(p):
		'expression : expression MSLASH expression'
		p[0] = OperacionBinariaCruzada(p,'Division Matriz')
		
	def p_expression_MMENOS(p):
		'expression : expression MMENOS expression'
		p[0] = OperacionBinariaCruzada(p,'Resta Matriz')
		
	def p_expression_MPORCENTAJE(p):
		'expression : expression MPORCENTAJE expression'
		p[0] = OperacionBinariaCruzada(p,'Modulo Matriz')
		
	def p_expression_MDIV(p):
		'expression : expression MDIV expression'
		p[0] = OperacionBinariaCruzada(p,'Division Entera Matriz')
		
	def p_expression_MMOD(p):
		'expression : expression MMOD expression'
		p[0] = OperacionBinariaCruzada(p,'Modulo Entero Matriz')
	
	
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
		'''expression : expression COMILLASIMPLE
			| LLAVESABRE parametros_matriz LLAVESCIERRA COMILLASIMPLE'''
		if len(p)==3:
			p[0] = Transpuesta(p[1])
		else:
			p[0] = Transpuesta(p[2])
	#--------------------------------------------------------------
	def p_parentesis(p):
		'expression : PARENTESISABRE expression PARENTESISCIERRA'
		p[0] = Agrupadores(p[2],'Abre Parentesis','Cierra Parentesis')
		
	
	def p_parametros_impresion(p):
		'''parametros_impresion : expression
					| string
					| expression COMA parametro
					| string COMA parametro'''
		if len(p)==2:
			p[0] = ListasSt(p[1],None)
		else:
			p[0] = ListasSt(p[1],p[3])
	
	def p_parametro(p):
		"""parametro : expression
					| expression COMA parametro"""
		if len(p)==2:
			p[0] = ListasSt(p[1],None)
		else:
			p[0] = ListasSt(p[1],p[3])
			
	def p_parametro_proyeccion(p):
		"""parametro_proyeccion : expression
					| expression COMA expression"""
		if len(p)==2:
			p[0] = ParametrosProyeccion(p[1],None)
		else:
			p[0] = ParametrosProyeccion(p[1],p[3])
		
	#------------------------------------------------------------------
	def p_llaves(p):
		'expression : LLAVESABRE parametros_matriz LLAVESCIERRA'	
		p[0] = Agrupadores(p[2],'Abre Llaves','Cierra Llaves')	
	
	def p_parametro_matriz(p):
		"""parametro_matriz : expression
					| expression COMA parametro_matriz"""
		if len(p)==2:
			p[0] = ParametrosMatriz(p[1],None)
		else:
			p[0] = ParametrosMatriz(p[1],p[3])
	
	def p_parametros_matriz(p):
		"""parametros_matriz : parametro_matriz
					| parametro_matriz DOSPUNTOS parametros_matriz"""
		if len(p)==2:
			p[0] = LiteralMatricial(p[1],None)
		else:
			p[0] = LiteralMatricial(p[1],p[3])
			
	#-----------------------------------------------------------------------
	def p_proyeccion(p):
		'expression : expression CORCHETEABRE parametro_proyeccion CORCHETECIERRA'
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
