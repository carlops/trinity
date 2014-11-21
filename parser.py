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
import math
from decimal import *
import pdb 
TFunciones = {}
##pdb.set_trace()
class Function:
	def __init__(self,Identificador, parametros, tipo, instrucciones,siguiente):
		self.Identificador = Identificador
		self.parametros = parametros
		self.tipo = tipo
		self.instrucciones = instrucciones
		self.siguiente= siguiente
		self.diccionario={}
		if self.parametros != None:
			self.diccionario=self.parametros.getDict();
		if  TFunciones.has_key(self.Identificador.getValor()):
			print ("Error: funcion '{}' ya declarada".format(self.Identificador.getValor()))
			exit(16)
		else:
			lista = []
			if self.parametros != None:
				lista = self.parametros.getParam([])
			
			lista.insert(0,self.tipo.check())
			TFunciones[self.Identificador.getValor()] = (lista,self.instrucciones)
		
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
		
	def check(self,tabla):
		scope = Alcance(self.Identificador,self.diccionario,tabla)
		if self.parametros != None:
			self.parametros.check(scope)
		if self.instrucciones != None:
			self.instrucciones.check(scope,TFunciones[self.Identificador.getValor()][0])
		if tabla==None:
			scope.Mostrar()
		self.siguiente.check(None)
		
class Program:
	def __init__(self,cuerpo):
		self.cuerpo=cuerpo

	def show(self, depth):
		print 'PROGRAM'
		self.cuerpo.show(depth+1)
		print 'END'
		
	def check(self,tabla):
		if self.cuerpo!=None:
			self.cuerpo.check(tabla)
			self.cuerpo.run(tabla)  ###### AQUI EMPIEZA EL RUN ######
	
	def run(self,pila):
		if self.cuerpo!=None:
			self.cuerpo.run(pila)
		
class Statement:
	pass
		
class Bloque(Statement):
	def __init__(self,declaraciones,instrucciones):
		self.declaraciones=declaraciones
		self.instrucciones=instrucciones
		self.diccionario={}
		self.diccionarioRun={}
		if self.declaraciones != None:
			self.diccionario=self.declaraciones.getDict()
			self.diccionarioRun = self.declaraciones.getDictRun()
			#print(self.diccionarioRun)
			#for i in self.diccionarioRun.items():
				#print(str(i[0])+': '+str(i[1].valor))
		
	def show(self,depth): ## este show hay que cambiarlo por check
		print('  '*depth+'USE:')
		self.declaraciones.show(depth+1)
		print('  '*depth+'IN:')
		self.instrucciones.show(depth+1)
		print('  '*depth+'END')
		
	def check(self,tabla):
		scope = Alcance(Variable('main'),self.diccionario,tabla)
		if self.declaraciones != None:
			self.declaraciones.check(scope)
		if self.instrucciones != None:
			self.instrucciones.check(scope)
		if tabla==None:
			scope.Mostrar()
			
	def run(self,pila):
		scope = Alcance(Variable('main'),self.diccionario,pila)
		if self.declaraciones != None:
			self.declaraciones.run(scope)
		if self.instrucciones != None:
			self.instrucciones.run(scope)
	
class Bloque_Fun(Statement):
	def __init__(self,declaraciones,instrucciones):
		self.declaraciones=declaraciones
		self.instrucciones=instrucciones
		self.diccionario={}
		self.diccionarioRun={}
		if self.declaraciones != None:
			self.diccionario=self.declaraciones.getDict()
			self.diccionarioRun = self.declaraciones.getDictRun()
		
	def show(self,depth): 
		print('  '*depth+'USE:')
		self.declaraciones.show(depth+1)
		print('  '*depth+'IN:')
		self.instrucciones.show(depth+1)
		print('  '*depth+'END')
		#self.check(self.scope)
		
	def check(self,tabla,funcion):
		scope = Alcance(Variable('fun'),self.diccionario,tabla)
		if self.declaraciones != None:
			self.declaraciones.check(scope)
		if self.instrucciones != None:
			self.instrucciones.check(scope,funcion)
		if tabla==None:
			scope.Mostrar()
		
	def run(self,pila):
		scope = Alcance(Variable('fun'),self.diccionario,pila)
		if self.declaraciones != None:
			self.declaraciones.run(scope)
		if self.instrucciones != None:
			self.instrucciones.run(scope)

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
			
	def run(self,pila):
		if self.ManyStatements == None:
			self.AnStatement.run(pila)
		else:
			self.AnStatement.run(pila)
			self.ManyStatements.run(pila)
	
	def to_str(self,string,pila):
		actual=self.AnStatement.run(pila)
		if isinstance(actual,str):
			if actual[0]=='"':
				actual=actual[1:-1]
				actual=actual.replace('\\"','"')
				actual=actual.replace('\\\\','\\')
				actual=actual.replace('\\n','\n')
				string +=actual
			else:
				string +=pila.buscar(actual).to_str()
		else:
			string +=actual.to_str()
		if self.ManyStatements == None:
			return string
		else:
			return self.ManyStatements.to_str(string,pila)
			
class ListasSt_Fun(Statement):
	def __init__(self, AnStatement, ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		
	def show(self, depth):
		if self.ManyStatements == None:
			self.AnStatement.show(depth)
		else:
			self.AnStatement.show(depth)
			self.ManyStatements.show(depth)
			
	def check(self, tabla,funcion):	
		if isinstance(self.AnStatement,Return) or isinstance(self.AnStatement,instruccion_IF_Fun) or isinstance(self.AnStatement,instruccion_FOR_Fun) or isinstance(self.AnStatement,instruccion_WHILE_Fun) or isinstance(self.AnStatement,Bloque_Fun):
			self.AnStatement.check(tabla,funcion)
		else:
			self.AnStatement.check(tabla)
			
		if self.ManyStatements != None:
				self.ManyStatements.check(tabla,funcion)
				
	def run(self,pila):
		res= self.AnStatement.run(pila)
		if isinstance(self.AnStatement,Return) or isinstance(res,tuple):
			if res[1]==True:
				return res
			return res
		if self.ManyStatements != None:
			p = self.ManyStatements.run(pila)
			return p
		
class ParametrosProyeccion(ListasSt):
	def check(self, tabla):
		primer=self.AnStatement.check(tabla)
		if not isinstance(primer,TNum):
			print('Error: proyeccion matricial, esperado tipo \'Numerico\' y recibido tipo {}'.format(primer.__class__.__name__))
			exit(10)
		if int(primer.getValor())<1:
			print('Error: proyeccion matricial, los indices deben ser mayores que uno')
			exit(10)
		if self.ManyStatements != None:
			segundo=self.ManyStatements.check(tabla)
			if not isinstance(segundo,TNum):
				print('Error: proyeccion matricial, esperado tipo \'Numerico\' y recibido tipo {}'.format(segundo.__class__.__name__))
				exit(10)
			if int(segundo.getValor())<1:
				print('Error: proyeccion matricial, los indices deben ser mayores que uno')
				exit(10)
		else:
			segundo = None
			
		return (primer, segundo)
	
	def run(self,pila):
		primer = self.AnStatement.run(pila).getValor()
		if self.ManyStatements != None:
			segundo = self.ManyStatements.run(pila).getValor()
		else:		
			segundo = None
		return (primer,segundo)
		
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
	
	def run(self,pila):
		fila=[]
		self.getFila(fila,pila)
		return fila
	
	def getFila(self,fila,pila):
		fila.append(self.UnParametro.run(pila))
		if self.OtrosParametros == None:
			return fila
		else:
			return self.OtrosParametros.getFila(fila,pila)
			#return fila.extend(self.OtrosParametros.getFila(fila))
		
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
	
	def getDictRun(self):
		self.clave =self.AnStatement.getValor()
		tipo=self.AnStatement.getTipo()
		if isinstance(tipo,TNum):
			self.IdValor[self.clave]=TNum(0)
		elif isinstance(tipo,TBool):
			self.IdValor[self.clave]=TBool(False)
		elif isinstance(tipo,TMatrix):
			col=int(tipo.getTamCol())
			fila=int(tipo.getTamFila())
			matriz=[[TNum(0) for x in range(col)] for x in range(fila)]
			self.IdValor[self.clave]=TMatrix(fila,col,matriz)
		else:
			exit(162)
		if self.ManyStatements != None:
			self.Aux = self.ManyStatements.getDictRun()
			for i in self.Aux:
				if self.clave != i:
					self.IdValor[i]=self.Aux[i]
		return self.IdValor
	
	def getParam(self,lista):
		lista.append(self.AnStatement.getTipo())
		if self.ManyStatements==None:
			return lista
		else:
			return self.ManyStatements.getParam(lista)
		
	def run(self,pila):
		self.AnStatement.run(pila)
		if self.ManyStatements != None:
			self.ManyStatements.run(pila)
		 
class LiteralMatricial(Statement):
	def __init__(self, parametroActual, restoParametros):
		self.parametroActual = parametroActual
		self.restoParametros = restoParametros
		self.NumFilas=1
		self.NumCol=0
		self.valor=[]
		
	def show(self, depth):
		if self.restoParametros == None:
			self.parametroActual.show(depth)
		else:
			self.parametroActual.show(depth)
			print(" "*(depth+4) + "DOSPUNTOS")
			self.restoParametros.show(depth)
		
	def check(self,tabla): 
		self.NumCol= self.parametroActual.check(tabla)
		self.NumFilas = self.checkMatriz(1,self.NumCol,tabla)
		filas = self.NumFilas
		columnas = self.NumCol
		self.valor = [[0 for x in range(self.NumCol)] for x in range(self.NumFilas)]
		return TMatrix(filas,columnas,[])
	
	def checkMatriz(self,filas,columnas,tabla):
		if columnas!= self.parametroActual.check(tabla):
			print("Error en Literal Matricial: las columnas deben tener la misma longitud")
			exit(9)
		if self.restoParametros != None:
			#col=col+ self.parametroActual.check(tabla)
			filas = filas + self.restoParametros.checkMatriz(filas,columnas,tabla)
		return filas
		
	def run(self,pila):
		matriz=[]
		matriz = self.getMatrix(pila,matriz)
		#filaActual= self.parametroActual.run(pila)
		#if not restoParametros== None
			#filaActual.extend(restoParametros.run(pila))
			#filasRestantes = self.checkMatriz(1,self.NumCol,pila)
		return TMatrix(self.NumFilas,self.NumCol,matriz)
	
	def getMatrix(self,pila,matriz):
		matriz.append(self.parametroActual.run(pila))
		if self.restoParametros == None:
			return matriz
		else:
			return self.restoParametros.getMatrix(pila,matriz)
	
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
		
	def check(self,tabla):
		tipo = self.condicion.check(tabla)
		if not isinstance(tipo,TBool):
			print ("Error: condicion de IF, esperado tipo 'Booleano' encontrado tipo '{}'".format(tipo.tipo))
			exit(12)
		if self.instrucciones != None:
			self.instrucciones.check(tabla)
		if self.instruccionesElse != None:
			self.instruccionesElse.check(tabla)
			
	def run(self,pila):
		cond = self.condicion.run(pila)
		if isinstance(cond,str):
			cond  = pila.buscar(cond)
		if cond.getValor():
			if self.instrucciones != None:
				self.instrucciones.run(pila)
		else:
			if self.instruccionesElse != None:
				self.instruccionesElse.run(pila)
			
class instruccion_FOR(Statement):
	def __init__(self,ID,estructura,instrucciones):
		self.ID= ID
		self.estructura = estructura
		self.instrucciones = instrucciones
		self.diccionario={}
		self.diccionario[self.ID.getValor()]=TNum(0);
		
	def show(self,depth):
		print('  '*depth+'FOR:')
		self.ID.show(depth+1)
		print('  '*depth + 'IN:')
		self.estructura.show(depth+1)
		print('  '*depth + 'DO:')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
	def check(self,tabla):
		scope = Alcance(self.ID,self.diccionario,tabla)
		if not isinstance(self.estructura.check(tabla),TMatrix):
			print('Error: en for, esperado tipo \'Matriz\', encontrado \'{}\''.format(self.estructura.check(scope).tipo))
			exit(15)
		if self.instrucciones != None:
			self.instrucciones.check(scope)
		if tabla==None:##########################################################
			scope.Mostrar()
			
	def run(self,pila):
		scope = Alcance(self.ID,self.diccionario,pila)
		tmatriz = self.estructura.run(pila)
		if isinstance(tmatriz,str):
			tmatriz = pila.buscar(tmatriz)
			
		matriz = tmatriz.getValor()
		for x in range(tmatriz.getTamFila()):
			for y in range(tmatriz.getTamCol()):
				scope.asignar(self.ID.getValor(),matriz[x][y])
				if self.instrucciones != None:
					self.instrucciones.run(scope)
		
	
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
		
	def check(self,tabla):
		tipo = self.condicion.check(tabla)
		if not isinstance(tipo,TBool):
			print ("Error: invalida condicion de WHILE, esperado tipo 'Booleano' encontrado tipo {}".format(tipo.tipo))
			exit(14)
		if self.instrucciones != None:
			self.instrucciones.check(tabla)
			
	def run(self,pila):
		cond = self.condicion.run(pila)
		if isinstance(cond,str):
			cond  = pila.buscar(cond)
			
		while cond.getValor() == True:
			if self.instrucciones != None:
				self.instrucciones.run(pila)
			cond = self.condicion.run(pila)
			if isinstance(cond,str):
				cond  = pila.buscar(cond)
		
		
# ------ CONTROL FUNCIONES --------
class instruccion_IF_Fun(Statement):
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
		
	def check(self,tabla,funcion):
		tipo = self.condicion.check(tabla)
		if not isinstance(tipo,TBool):
			print ("Error: condicion de IF, esperado tipo 'Booleano' encontrado tipo '{}'".format(tipo.tipo))
			exit(12)
		if self.instrucciones != None:
			self.instrucciones.check(tabla,funcion)
		if self.instruccionesElse != None:
			self.instruccionesElse.check(tabla,funcion)
			
	def run(self,pila):
		cond = self.condicion.run(pila)
		if isinstance(cond,str):
			cond  = pila.buscar(cond)
		if cond.getValor():
			if self.instrucciones != None:
				p = self.instrucciones.run(pila)
				return p
		else:
			if self.instruccionesElse != None:
				return self.instruccionesElse.run(pila)
			
class instruccion_FOR_Fun(Statement):
	def __init__(self,ID,estructura,instrucciones):
		self.ID= ID
		self.estructura = estructura
		self.instrucciones = instrucciones
		self.diccionario={}
		self.diccionario[self.ID.getValor()]=TNum(self.ID.getValor());
		
	def show(self,depth):
		print('  '*depth+'FOR:')
		self.ID.show(depth+1)
		print('  '*depth + 'IN:')
		self.estructura.show(depth+1)
		print('  '*depth + 'DO:')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
	def check(self,tabla, funcion):
		scope = Alcance(self.ID,self.diccionario,tabla)
		if not isinstance(self.estructura.check(tabla),TMatrix):
			print('Error: en for, esperado tipo \'Matriz\', encontrado \'{}\''.format(self.estructura.check(scope).tipo))
			exit(15)
		if self.instrucciones != None:
			self.instrucciones.check(scope,funcion)
		if tabla==None:########################################################### ToDo BORRAR
			scope.Mostrar()
		
	def run(self,pila):
		scope = Alcance(self.ID,self.diccionario,pila)
		tmatriz = self.estructura.run(pila)
		if isinstance(tmatriz,str):
			tmatriz = pila.buscar(tmatriz)
			
		matriz = tmatriz.getValor()
		for x in range(tmatriz.getTamFila()):
			for y in range(tmatriz.getTamCol()):
				scope.asignar(self.ID.getValor(),matriz[x][y])
				if self.instrucciones != None:
					res = self.instrucciones.run(scope)
					if isinstance(res,tuple):
						return res
	
class instruccion_WHILE_Fun(Statement):
	def __init__(self, condicion,instrucciones):
		self.condicion = condicion
		self.instrucciones = instrucciones
		
	def show(self, depth):
		print('  '*depth+'WHILE:')
		self.condicion.show(depth+1)
		print('  '*depth + 'DO:')
		self.instrucciones.show(depth+1)
		print('  '*depth + 'END')
		
	def check(self,tabla,funcion):
		tipo = self.condicion.check(tabla)
		if not isinstance(tipo,TBool):
			print ("Error: invalida condicion de WHILE, esperado tipo 'Booleano' encontrado tipo {}".format(tipo.tipo))
			exit(14)
		self.instrucciones.check(tabla,funcion)
		
	def run(self,pila):
		cond = self.condicion.run(pila)
		if isinstance(cond,str):
			cond  = pila.buscar(cond)
			
		while cond.getValor() == True:
			if self.instrucciones != None:
				res=self.instrucciones.run(pila)
				if isinstance(res,tuple):
					return res
			cond = self.condicion.run(pila)
			if isinstance(cond,str):
				cond  = pila.buscar(cond)
		
#------------------------------------------------------------------
		
class Read(Statement):
	def __init__(self, Identificador):
		self.Identificador = Identificador
	def show(self, depth):
		print ('  '*depth + 'Lectura:')
		self.Identificador.show(depth+1)
	def check(self,tabla):
		tipo = self.Identificador.check(tabla)
		if isinstance(tipo,TMatrix):
			print ("Error: invalida operacion con 'read' identificador del tipo 'Matriz'")
			exit(14)
			
	def run(self,pila):
		iden = self.Identificador.run(pila)
		if isinstance(iden,str):
			val = pila.buscar(iden)
		else:
			print("Error: invalido uso del comando 'read', una variable debe ser otorgada")
			exit(139)
		raw = raw_input()
		
		if isinstance(val,TNum):
			match = re.match(r'(\d+(\.\d+)?)', raw)
			if match:
				valor = Decimal(match.group())
				asig = TNum(valor)
				pila.asignar(iden,asig)
				return asig
			else:
				print ("Error: invalido valor ingresado, esperado tipo 'Numerico'")
				exit(140)
		elif isinstance(val,TBool):
			matchT = re.match(r'true\b',raw)
			matchF = re.match(r'false\b',raw)
			
			if matchT:
				asig = TBool(True)
				pila.asignar(iden,asig)
				return asig
			elif matchF:
				asig = TBool(False)
				pila.asignar(iden,asig)
				return asig
			else:
				print("Error: invalido valor ingresado, esperado tipo 'Booleano'")
				exit(141)
		else:
			print("Error: invalido valor ingresado, Abortando programa")
			exit(142)
				
class Print(Statement):
	def __init__(self,parametros):
		self.parametros = parametros
		
	def show(self, depth):
		print('  '*depth + 'Print:')
		self.parametros.show(depth + 1)
		
	def check(self,tabla):
		self.parametros.check(tabla)
		
	def run (self,pila):
		string=''
		print (self.parametros.to_str(string,pila))
	
class Return(Statement):
	def __init__(self,statement):
		self.statement = statement
		
	def show(self, depth):
		print('  '*depth + 'Return:')
		self.statement.show(depth + 1)
		
	def check(self, tabla,funcion):
		tipo = self.statement.check(tabla)
		if not isinstance(funcion[0],tipo.__class__):
			print("Error: tipo en instruccion 'return', esperado tipo {} encontrado tipo {}".format(funcion[0].tipo,tipo.tipo))
			exit(22)
		if isinstance(tipo,TMatrix):
			filafun = funcion[0].getTamFila()
			filatipo = tipo.getTamFila()
			colfun = funcion[0].getTamCol()
			coltipo = tipo.getTamCol()
			
			if filafun != filatipo or colfun != coltipo:
				print ("Error: dimensiones de la matriz de retorno no concuerdan con las definidas por la funcion")
				exit(22)
				
	def run(self,pila):
		#pdb.set_trace()
		val = self.statement.run(pila)
		if isinstance(val,str):
			val = pila.buscar(val)
		return (val,True)
		
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
				print ("Error: esperado tipo Booleano, encontrado {} ".format(tipo))
				exit(13)
		else:
			if not (isinstance(tipo,TNum) or isinstance(tipo,TMatrix)):
				print ("Error: esperado tipo 'Numerico' o 'Matriz', encontrado {}".format(tipo))
				exit(13)
		return tipo
	
	def run(self,pila):
		valor = self.hijo.run(pila)
		if isinstance(valor,str):
			valor  = pila.buscar(valor)
		if self.name == 'Negacion':
			return TBool(not valor.getValor())
		else:# Es Matriz o Numero
			if isinstance(valor,TMatrix): 
				matriz = valor.getValor()
				mTotal = [[0 for x in range(valor.getTamCol())] for x in range(valor.getTamFila())]
				for i in range(valor.getTamFila()):
					for j in range(valor.getTamCol()):
						mTotal[i][j] = TNum(-1 * matriz[i][j].getValor())
				return TMatrix(valor.getTamFila(),valor.getTamCol(),mTotal)
			elif isinstance(valor,TNum):
				return TNum(-1*valor.getValor())
			else:
				exit(182)
			
		
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
	
	def run(self,pila):
		return self.expresion.run(pila)
	
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
		
	def check(self,tabla):
		tipoE= self.expresion.check(tabla)
		if not isinstance(tipoE,TMatrix):
			print("Error: invalida proyeccion, identificador del tipo {} y esperado del tipo 'Matriz'".format(tipoE.tipo))
			exit(15)
		parametros =  self.parametros.check(tabla)
		error=False
		fila=tipoE.getTamFila()
		col =tipoE.getTamCol()
		if parametros[1]==None:
			if col==1 and fila<parametros[0]:
				error=True
			elif fila==1 and col<parametros[0]:
				error=True
		else:
			if fila<int(parametros[0].getValor()) or col<int(parametros[1].getValor()):
				error=True
		if error:
			print('Error: Proyeccion no esta dentro del rango definido para la matriz')
			exit(10)
		return TNum(0)
	
	def run(self,pila):
		iden = self.expresion.run(pila)
		if isinstance(iden,str):
			tmatriz = pila.buscar(iden)
		else:
			tmatriz = iden
			
		valor = tmatriz.getValor()
		proy = self.parametros.run(pila)
		
		if proy[1] == None:
			if tmatriz.getTamFila()==1:
				return valor[0][int(proy[0])-1]
			elif tmatriz.getTamCol()==1:
				return valor[int(proy[0])-1][0]
			else:
				exit(250)
		else:
			return valor[int(proy[0])-1][int(proy[1])-1]
		
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
	
	def run(self,pila):
		izq = self.hijos['operando izquierdo'].run(pila)
		der = self.hijos['operando derecho'].run(pila)
		
		if isinstance(izq,str):
			izq = pila.buscar(izq)
			
		if isinstance(der,str):
			der = pila.buscar(der)
		
		if der.run(pila)==0:
				exit(100)
				
		if self.name == 'Division':
			return TNum(izq.run(pila) / der.run(pila))
		elif self.name == 'Modulo':
			return TNum(izq.run(pila) % der.run(pila))
		elif self.name == 'Division Entera':
			return TNum(izq.run(pila) // der.run(pila))
		elif self.name == 'Modulo Entero':
			return TNum(math.floor(izq.run(pila) % der.run(pila)))
		else:
			exit (101)
	
	def equals(self,izq,der,operador):
		if (isinstance(izq,TNum) and isinstance(der,TNum)):
			return izq
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
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
			print ("Error: las expresiones {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
			exit(15)
			
	def run(self,pila):
		izq = self.hijos['operando izquierdo'].run(pila)
		der = self.hijos['operando derecho'].run(pila)
		
		if isinstance(izq,str) and isinstance(der,TNum):
			matriz = pila.buscar(izq)
			num = der.getValor()
		elif isinstance(der,str) and isinstance(izq,TNum):
			matriz = pila.buscar(der)
			num = izq.getValor()
		elif isinstance(izq,TMatrix) and isinstance(der,TNum):
			matriz = izq
			num = der.getValor()
		elif isinstance(der,TMatrix) and isinstance(izq,TNum):
			matriz = der
			num = izq.getValor()
		else:
			exit(243)
			
		valor = matriz.getValor()
		mTotal = [[0 for x in range(matriz.getTamCol())] for x in range(matriz.getTamFila())]
		if self.name== 'Suma Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					mTotal[i][j] = TNum(valor[i][j].getValor() + num)
					
		elif self.name == 'Resta Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					if isinstance(izq,str) or isinstance(izq,TMatrix):
						mTotal[i][j] = TNum(valor[i][j].getValor()-num)
					else:
						mTotal[i][j] = TNum(num - valor[i][j].getValor())
						
		elif self.name == 'Division Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					if isinstance(izq,str) or isinstance(izq,TMatrix):
						if num == 0:
							exit(242)
						mTotal[i][j] = TNum(valor[i][j].getValor() / num)
					else:
						if valor[i][j].getValor() == 0:
							exit(241)
						mTotal[i][j] = TNum(num / valor[i][j].getValor())
						
		elif self.name == 'Multiplicacion Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					mTotal[i][j] = TNum(valor[i][j].getValor()*num)
					
		elif self.name == 'Division Entera Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					if isinstance(izq,str) or isinstance(izq,TMatrix):
						if num == 0:
							exit(240)
						mTotal[i][j] = TNum(valor[i][j].getValor() // num)
					else:
						if valor[i][j].getValor() == 0:
							exit(239)
						mTotal[i][j] = TNum(num // valor[i][j].getValor())
						
		elif self.name == 'Modulo Matriz':
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					if isinstance(izq,str) or isinstance(izq,TMatrix):
						mTotal[i][j] = TNum(valor[i][j].getValor() % num)
						if num == 0:
							exit(238)
					else:
						if valor[i][j].getValor() == 0:
							exit(237)
						mTotal[i][j] = TNum(num % valor[i][j].getValor())
						
		elif self.name == 'Modulo Entero Matriz':#################
			for i in range(matriz.getTamFila()):
				for j in range(matriz.getTamCol()):
					if isinstance(izq,str) or isinstance(izq,TMatrix):
						if num == 0:
							exit(236)
						mTotal[i][j] = TNum(math.floor(valor[i][j].getValor()%num))
					else:
						if valor[i][j].getValor() == 0:
							exit(235)
						mTotal[i][j] = TNum(math.floor(num % valor[i][j].getValor()))
		else:
			exit(187)
			
		return TMatrix(matriz.getTamFila(),matriz.getTamCol(),mTotal)

class OperacionBinariaSRM(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		operandoder = self.hijos['operando derecho'].check(tabla)
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
					return TMatrix(izq.TamFila,der.TamColumna,[])
				else:
					print ("Error: dimensiones de matrices incorrectas, no pueden ser operadas con el operador {} ".format(operador))
					exit(6)
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
			exit(6)
			
	def run(self,pila):
		izq = self.hijos['operando izquierdo'].run(pila)
		der = self.hijos['operando derecho'].run(pila)
		if isinstance(izq,str):
			izq = pila.buscar(izq)
			
		if isinstance(der,str):
			der = pila.buscar(der)
		
		if isinstance(izq,TMatrix):
			mIzq=izq.getValor()
			mDer=der.getValor()
			if self.name=='Suma':
				mTotal= [[0 for x in range(izq.getTamCol())] for x in range(izq.getTamFila())]
				for row in range(izq.getTamCol()):
					for col in range(izq.getTamFila()):
						mTotal[col][row]=TNum(mIzq[col][row].run(pila) + mDer[col][row].run(pila) )
				return TMatrix(izq.getTamFila(),izq.getTamCol(),mTotal)
			
			elif self.name=='Resta':
				mTotal= [[0 for x in range(izq.getTamCol())] for x in range(izq.getTamFila())]
				for row in range(izq.getTamCol()):
					for col in range(izq.getTamFila()):
						mTotal[col][row]=TNum(mIzq[col][row].run(pila) - mDer[col][row].run(pila) )
				return TMatrix(izq.getTamFila(),izq.getTamCol(),mTotal)
			elif self.name=='Multiplicacion': ###### hay que ponerla como es #######
				mTotal= [[0 for x in range(der.getTamCol())] for x in range(izq.getTamFila())]
				for row in range(izq.getTamFila()):
					for x in range(der.getTamCol()):
						for col in range(der.getTamFila()): ######## ToDo res no  es TNum ####
							mTotal[row][x] += (mIzq[row][col].run(pila) * mDer[col][x].run(pila))
						mTotal[row][x] = TNum(mTotal[row][x])
				return TMatrix(izq.getTamFila(),der.getTamCol(),mTotal)
			else:
				exit(222)
			
		elif isinstance(izq,TNum):
			if self.name=='Suma':
				return TNum(izq.run(pila) + der.run(pila))
			elif self.name=='Resta':
				return TNum(izq.run(pila) - der.run(pila))
			elif self.name=='Multiplicacion':
				return TNum(izq.run(pila) * der.run(pila))
			else:
				exit(223)
		else:
			exit(224)
			
class OperacionBinariaComp(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		operandoder = self.hijos['operando derecho'].check(tabla)
		if not isinstance(operandoizq,TNum) or not isinstance(operandoder,TNum):
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(operandoizq.tipo,operandoder.tipo,self.name))
			exit(6)
		return TBool('true')
	
	def run(self, pila):
		izq = self.hijos['operando izquierdo'].run(pila)
		if isinstance(izq,str):
			izq = pila.buscar(izq)
		der = self.hijos['operando derecho'].run(pila)
		if isinstance(der,str):
			der = pila.buscar(der)
		if self.name == '>=':
			return TBool(izq.run(pila) >= der.run(pila))
		elif self.name == '>':
			return TBool(izq.run(pila) > der.run(pila))
		elif self.name == '<=':
			return TBool(izq.run(pila) <= der.run(pila))
		elif self.name == '<':
			return TBool(izq.run(pila) < der.run(pila))
		else:
			exit(178)
	
class OperacionBinariaIgualdad(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		operandoder = self.hijos['operando derecho'].check(tabla)
		return self.equals(operandoizq,operandoder,self.name)
	
	def equals(self,izq,der,operador):
		if isinstance(izq,der.__class__):
			return TBool('true')
		else:
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
			exit(6)
			
	def run(self,pila):
		izq = self.hijos['operando izquierdo'].run(pila)
		if isinstance(izq,str):
			izq = pila.buscar(izq)
		der = self.hijos['operando derecho'].run(pila)
		if isinstance(der,str):
			der = pila.buscar(der)
			
		if isinstance(izq,TMatrix):
			filader=der.getTamFila()
			filaizq=izq.getTamFila()
			colder=der.getTamCol()
			colizq=izq.getTamCol()
			izq = izq.run(pila)
			der = der.run(pila)
			if self.name =='==':
				if filader==filaizq and colder==colizq:
					for i in range(filader):
						for j in range(colder):
							if izq[i][j]!=der[i][j]:
								return TBool(False)
					return TBool(True)
				else:
					return TBool(False)
			elif self.name =='/=':
				if filader==filaizq and colder==colizq:
					for i in range(filader):
						for j in range(colder):
							if izq[i][j]!=der[i][j]:
								return TBool(True)
					return TBool(False)
				else:
					return TBool(True)
			else:
				exit(126)
		elif isinstance(izq,TNum):
			if self.name =='==':
				return TBool(izq.run(pila) == der.run(pila))
			elif self.name =='/=':
				return TBool(izq.run(pila) != der.run(pila))
			else:
				exit(125)
		elif isinstance(der,TBool):
			if self.name =='==':
				return TBool(izq.run(pila) == der.run(pila))
			elif self.name =='/=':
				return TBool(izq.run(pila) != der.run(pila))
			else:
				exit(124)
		else:
			exit(123)
		
class OperacionBinariaOpBool(OperacionBinaria):
	def check(self,tabla):
		operandoizq = self.hijos['operando izquierdo'].check(tabla)
		operandoder = self.hijos['operando derecho'].check(tabla)
		if not isinstance(operandoizq,TBool):
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
			exit(12)
		if not isinstance(operandoder,TBool):
			print ("Error: las expresiones  {} y {} no pueden ser operadas con el operador {} ".format(izq.tipo,der.tipo,operador))
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
	
	def run(self,pila):
		var = self.hijos['variable'].run(pila)
		valor=self.hijos['expresion'].run(pila)
		if isinstance(valor,str):
			valor = pila.buscar(valor)
		pila.asignar(var,valor)
		return valor
		
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
			exit(10)
		parametros = self.proyeccion.check(tabla)#Verifica que sean numericos
		error=False
		fila=ladoIzq.getTamFila()
		col =ladoIzq.getTamCol()
		if parametros[1]==None:
			if col==1 and fila<parametros[0]:
				error=True
			elif fila==1 and col<parametros[0]:
				error=True
		else:
			if fila<int(parametros[0].getValor()) or col<int(parametros[1].getValor()):
				error=True
		if error:
			print('Error: Proyeccion no esta dentro del rango definido para la matriz')
			exit(10)
		ladoDer = self.expresion.check(tabla)
		if not isinstance(ladoDer,TNum):
			print("Error: asginacion a matriz esperado tipo 'Numerico' y encontrado "+ ladoDer.tipo)
			exit(10)
			
	def run(self,pila):
		iden = self.Identificador.run(pila)
		if isinstance(iden,str):
			tmatriz = pila.buscar(iden)
		else:
			tmatriz = iden
		valor = tmatriz.getValor()
		exp = self.expresion.run(pila)
		
		proy = self.proyeccion.run(pila)
		if proy[1] == None:
			if tmatriz.getTamFila()==1:
				valor[0][int(proy[0])-1] = exp
			elif tmatriz.getTamCol()==1:
				valor[int(proy[0])-1][0] = exp
			else:
				exit(250)
		else:
			valor[int(proy[0])-1][int(proy[1])-1] = exp
		tmatriz.setValor(valor)
		if isinstance(iden,str):
			pila.asignar(iden,tmatriz)
		return tmatriz
		
		
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
		
		fila = tipo.getTamFila()
		col = tipo.getTamCol()
		return TMatrix(col,fila,[])
	
	def run(self,pila):
		matriz  = self.valor.run(pila)
		if isinstance(matriz,str):
			matriz = pila.buscar(matriz)
		mTotal = [[0 for x in range(matriz.getTamFila())] for x in range(matriz.getTamCol())]
		valor = matriz.getValor()
		for i in range(matriz.getTamFila()):
			for j in range(matriz.getTamCol()):
				mTotal[j][i] = valor[i][j]
		return TMatrix(matriz.getTamCol(),matriz.getTamFila(),mTotal)
		
		
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
	def run(self,pila):
		return TNum(Decimal(self.valor))
	
class Booleano(Expresion):
	def __init__(self,booleano):
		self.valor = booleano
	def show(self, depth):
		print('  '*depth + 'Booleano:\n'+'  '*(depth+1) + 'valor: '+str(self.valor))
	def check(self,tabla):
		return TBool(self.valor)
	def getValor(self):
		return self.valor
	def run(self,pila):
		if self.valor=='true':
			return TBool(True)
		elif self.valor=='false': 
			return TBool(False)
		else:
			exit(160)
	
class String(Expresion):
	def __init__(self,valor):
		self.valor = valor
	def show(self,depth):
		print ('  '*depth + 'String: '+ str(self.valor))
	def check(self,tabla):
		pass
	def getValor(self):
		return self.valor
	def run(self,valor):
		return self.valor
	
class LiteralFuncion(Expresion):
	def __init__(self,Identificador,parametros):
		self.Identificador = Identificador
		self.parametros = parametros
		
	def check(self,tabla):
		fun = self.Identificador.getValor()
		if not TFunciones.has_key(fun):
			print("Error: funcion '{}' no declarada".format(fun))
			exit(16)
		parametrosFun = TFunciones[fun][0]
		if self.parametros != None:
			return self.parametros.check(tabla,parametrosFun)
		elif len(parametrosFun)==1 and self.parametros == None:
			return parametrosFun[0]
		elif len(parametrosFun)>1 and self.parametros == None:
			print ("Error: numero de parametros invalido en llamada a funcion")
			exit(17)
			
	def run(self,pila):
		fun = TFunciones[self.Identificador.getValor()]
		diccionario = {}
		parametros = fun[0][1:]
		instrucciones = fun[1]
		diccionario = self.parametros.run(pila,parametros)
		scope = Alcance(self.Identificador.getValor(),diccionario,None)
		res = instrucciones.run(scope)
		if isinstance(res,tuple):
			return res[0]
		return res
	
class ParametrosFuncion(Expresion):
	def __init__(self,AnStatement,ManyStatements):
		self.AnStatement = AnStatement
		self.ManyStatements = ManyStatements
		self.size = self.getSize()
		
	def check(self,tabla,param):
		if self.size != len(param)-1:
			print ("Error: numero de parametros invalido en llamada a funcion")
			exit(17)
			
		tipo1 = self.AnStatement.check(tabla)
		lista = []
		lista = self.getParam(lista,tabla)
		
		for ind,x in enumerate(lista):
			if param[ind+1].tipo != x.tipo:
				print("Error: invalido pase de parametro en invocacion a funcion, esperado tipo '{}' encontrado tipo '{}'".format(param[ind+1].tipo, x.tipo))
				exit(17)
			if isinstance(x,TMatrix):
				filaparam=param[ind+1].getTamFila()
				filax=x.getTamFila()
				colparam=param[ind+1].getTamCol()
				colx=x.getTamCol()
				
				if int(filaparam) != int(filax) or int(colparam) != int(colx):
					print("Error: invalido pase de parametros en invocacion a funcion, matriz proporsionada de dimensiones invalidas")
					exit(17)
					
		return param[0]
	
	def run(self,pila,param):
		dic = {}
		lista = []
		lista = self.getParamRun(lista,pila)
		for ind,x in enumerate(param):
			dic[x.getValor().getValor()] = lista[ind]
		return dic
	
		
	def getParam(self,lista,tabla):
		lista.append(self.AnStatement.check(tabla))
		if self.ManyStatements==None:
			return lista
		else:
			return self.ManyStatements.getParam(lista,tabla)

	def getParamRun(self,lista,pila):
		val = self.AnStatement.run(pila)
		if isinstance(val,str):
			val = pila.buscar(val)
		lista.append(val)
		if self.ManyStatements==None:
			return lista
		else:
			return self.ManyStatements.getParamRun(lista,pila)
		
	def getSize(self):
		if self.ManyStatements == None:
			return 1
		else:
			return 1+self.ManyStatements.getSize()
		
#--------------- DECLACARACIONES
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
	
	def run(self,pila):
		if self.expresion!=None:
			valor=self.expresion.run(pila)
			pila.inicializacion(self.nombre.valor,valor)
			return valor
		else:
			#Inicializacion por defecto
			tipo=self.getTipo()
			if isinstance(tipo,TBool):
				valor=False
			elif isinstance(tipo,TNum):
				valor=0
			elif isinstance(tipo,TMatrix):
				print(self.getValor)
				valor=[[0]]
			else:
				exit(123)
			return valor
		
class Type(Statement):
	def __init__(self,tipo,fila,col):
		self.tipo = tipo
		self.fila = fila
		self.col = col
	def show(self,depth):
		pass
	def check(self):
		if self.tipo == 'number':
			return TNum('0')
		elif self.tipo == 'boolean':
			return TBool('false')
		else:
			if  (self.fila!=None):
				if (isinstance(self.fila,LiteralNumerico)):
					if '.' in (self.fila.getValor()):
						print('Error: invalido retorno de funcion, parametro de matriz esperado tipo Entero')
						exit(21)
					else:
						if int(self.fila.getValor()) <1:
							print('Error: invalido retorno de funcion, la cantidad de filas debe ser positiva')
							exit(21)
				else:
					print('Error: invalido retorno de funcion, esperado tipo Numerico en parametro, encontrado tipo {}'.format(self.fila))
					exit(21)
				
			if (self.col!=None):
				if isinstance(self.col,LiteralNumerico):
					if '.' in (self.col.getValor()):
						print('Error: invalido retorno de funcion, parametro de matriz esperado tipo Entero')
						exit(21)
					else:
						if int(self.col.getValor()) <1:
							print('Error: invalido retorno de funcion, la cantidad de columnas debe ser positiva')
							exit(21)
				else:
					print('Error: invalido retorno de funcion, esperado tipo Numerico en parametro, encontrado tipo {}'.format(self.col))
					exit(21)
			if self.tipo == 'matrix':
				return TMatrix(self.fila.valor,self.col.valor,[])
			elif self.tipo == 'col':
				return TMatrix(self.fila.valor,'1',[])
			elif self.tipo == 'row':
				return TMatrix('1',self.col.valor,[])
			else:
				print("Error: tipo de retorno invalido: {}".format(tipo))
				exit(21)
		
class DeclaracionMatriz(Statement):
	def __init__(self,Identificador,fila,col,expresion):
		self.Identificador = Identificador
		self.fila = fila
		self.col = col
		self.expresion = expresion
		self.tipo = 'Matriz'
	
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
		return TMatrix(self.fila.valor,self.col.valor,self.Identificador)
	
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
		
	def run(self,pila):
		if self.expresion!=None:
			valor=self.expresion.run(pila)
			pila.inicializacion(self.Identificador.valor,valor)
			return valor
		return None
		
	
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
		return TMatrix(self.fila.valor,self.col.valor,self.valor)
	
	def run(self,pila):
		if self.expresion!=None:
			valor=self.expresion.run(pila)
			pila.inicializacion(self.Identificador.valor,valor)
			return valor
		return None

class Variable(Expresion): 
	def __init__(self,valor):
		self.valor = valor
	def show(self, depth):
		print('  '*depth + 'Identificador:\n' + '  '*(depth+1) + 'nombre: '+str(self.valor))
	def check(self,tabla):
		if tabla != None:
			return tabla.buscar(self.valor)
		else:
			print ("Error: uso de varible no declarada '{}'".format(self.valor))
			exit(16)
	def getValor(self):
		return self.valor
	def run(self,pila):
		return self.valor
		#return pila.buscar(self.valor)
	
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
	def setValor(self,valor):
		self.valor = valor
	def run(self,pila):
		return Decimal(self.valor)
	def to_str(self):
		return str(Decimal(self.valor))
	
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
	def run(self,pila):
		return self.valor
	def setValor(self,valor):
		self.valor = valor
	def to_str(self):
		return str(self.valor)
			
class TMatrix(Tipo):
	tipo = 'Matriz'
	def __init__(self,TamFila,TamColumna,valor):
		self.TamFila=TamFila
		self.TamColumna=TamColumna
		self.valor=valor
		
	def getTamFila(self):
		return self.TamFila
	
	def setTamFila(self,valor):
		self.getTamFila = valor
		
	def getTamCol(self):
		return self.TamColumna
	
	def setTamCol(self,valor):
		self.TamColumna = valor
	
	def getTipo(self):
		return self.tipo
	
	def toStr(self):
		return '{}({},{})'.format(self.tipo,self.TamFila,self.TamColumna)

	def getValor(self):
		return self.valor
	
	def setValor(self,valor):
		self.valor = valor
		
	def run(self,pila):
		return self.getValor()
	
	def to_str(self):
		string='['
		for row in range(self.TamFila):
			#if row==0:
			string+='['
			for col in range(self.TamColumna):
				string += str(self.valor[row][col].to_str())
				if col!=self.TamColumna-1:
					string +=','
				else:
					string +=']'
			if row==self.TamFila-1:
				string +=']'
		return string
	
class Alcance: #decls se crea al ver un USE o un FOR
	def __init__ (self,nombre,decls,padre):
		self.nombre = nombre
		self.locales={}
		self.padre=padre
		self.nivel=self.getNivel(self.padre)
		for key in decls: 
			self.locales[key]=decls[key]
		self.hijos=[]
		if self.padre != None:
			self.padre.hijos.append(self)
	
	def getNivel(self,tabla):
		if tabla==None:
			return 0
		else:
			return 1 + self.getNivel(tabla.padre)
	
	def Mostrar(self):
		depth=' '*self.nivel*2
		if TFunciones.has_key(self.nombre.getValor()) or (self.nombre.getValor()=='main' and self.nivel==0):
			print(depth+'Alcance '+self.nombre.getValor() +':')
		else:
			print(depth+'Alcance '+str(self.nivel) +':')
		self.nivel=self.nivel*2
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
	
	def inicializacion(self,var,valor):
		self.locales[var]=valor
		#if var in self.locales:
		#else:
			#self.locales[var]=valor
			
	def asignar(self,var,valor):
		if var in self.locales:
			self.locales[var]=valor
		elif self.padre != None:
			return self.padre.asignar(var,valor)
		else:
			exit(102)
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
			| FUNCTION ID PARENTESISABRE statement_decl_param PARENTESISCIERRA RETURN type BEGIN function_statement_list END PUNTOYCOMA program
			| PROGRAM END PUNTOYCOMA
			| FUNCTION ID PARENTESISABRE PARENTESISCIERRA RETURN type BEGIN END PUNTOYCOMA program
			| FUNCTION ID PARENTESISABRE statement_decl_param PARENTESISCIERRA RETURN type BEGIN END PUNTOYCOMA program
			|  FUNCTION ID PARENTESISABRE PARENTESISCIERRA RETURN type BEGIN function_statement_list  END PUNTOYCOMA program'''
		if len(p)==5:
			p[0] = Program(p[2])
		elif len(p)==13:
			p[0] = Function(Variable(p[2]), p[4], p[7],p[9],p[12])
		elif len(p)==4:
			p[0] = Program(None)
		elif len(p)==11:
			p[0] = Function(Variable(p[2]),None,p[6],None,p[10])
		elif len(p)==12:
			if p[5] == 'return':
				p[0] = Function(Variable(p[2]), None, p[6], p[8],p[11])
			else:
				p[0] = Function(Variable(p[2]),p[4], p[7], None,p[11])
			
	#-----------------------------------------------------------------------------------
	### FUNCTION statements
	
	def p_function_call(p):
		'''expression : ID PARENTESISABRE parametro_funcion PARENTESISCIERRA
							| ID PARENTESISABRE PARENTESISCIERRA'''
		if len(p) == 5:
			p[0] = LiteralFuncion(Variable(p[1]),p[3])
		else:
			p[0] = LiteralFuncion(Variable(p[1]),None)
		
	def p_bloque_function(p):
		'''function_statement : USE statement_decl_list IN function_statement_list END
					| USE IN function_statement_list END
					| USE statement_decl_list IN END
					| USE IN END'''
		if len(p) == 6:
			p[0]=Bloque_Fun(p[2],p[4])
		elif len(p) == 5 and p[2] == 'in':
			p[0] = Bloque_Fun(None,p[3])
		elif len(p) == 5 and isinstance(p[2],ListasSt_Dcl):
			p[0] = Bloque_Fun(p[2],None)
		elif len(p) == 4:
			p[0] = Bloque_Fun(None, None)
		
	def p_parametro_function(p):
		"""parametro_funcion : expression
					| expression COMA parametro_funcion"""
		if len(p)==2:
			p[0] = ParametrosFuncion(p[1],None)
		else:
			p[0] = ParametrosFuncion(p[1],p[3])
			
	def p_function_statement_list(p):
		'''function_statement_list : function_statement PUNTOYCOMA
					| function_statement PUNTOYCOMA function_statement_list'''
		if len(p)==3:
			p[0]=ListasSt_Fun(p[1],None)
		else:
			p[0]=ListasSt_Fun(p[1] ,p[3])
	
	def p_function_RETURN(p):
		'function_statement : RETURN expression'
		p[0] = Return(p[2])
		
	def p_function_statement_expresion(p):
		'''function_statement : expression'''
		p[0]=p[1]
		
	def p_function_statement_READ(p):
		'function_statement : READ ID'
		p[0] = Read(Variable(p[2]))
		
	def p_function_statement_PRINT(p):
		'function_statement : PRINT parametros_impresion'
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
					| IF expression THEN function_statement_list END
					| IF expression THEN ELSE END
					| IF expression THEN function_statement_list ELSE END
					| IF expression THEN ELSE function_statement_list END
					| IF expression THEN END'''
		if len(p) == 8:
			p[0] = instruccion_IF_Fun(p[2],p[4],p[6])
		elif (len(p)==6 and isinstance(p[4], ListasSt_Fun)) or (len(p)==7 and isinstance(p[4],ListasSt_Fun)):
			p[0] = instruccion_IF_Fun(p[2],p[4],None)
		elif (len(p)==6 and p[4]=='else') or len(p) == 5:
			p[0] = instruccion_IF_Fun(p[2],None,None)
		elif len(p)==7 and p[4] == 'else':
			p[0] = instruccion_IF_Fun(p[2],None,p[5])
	
	def p_fuction_FOR(p):
		'''function_statement : FOR ID IN expression DO function_statement_list END
					| FOR ID IN expression DO END'''
		if len(p)== 8:
			p[0] = instruccion_FOR_Fun(Variable(p[2]),p[4],p[6])
		else:
			p[0] = instruccion_FOR_Fun(Variable(p[2]),p[4],None)
		
	def p_function_WHILE(p):
		'''function_statement : WHILE expression DO function_statement_list END
					| WHILE expression DO END'''
		if len(p) == 6:
			p[0] = instruccion_WHILE_Fun(p[2], p[4])
		else:
			p[0] = instruccion_WHILE_Fun(p[2], None)
	
	#-----------------------------------------------------------------------------------
	### STATEMENTS
	def p_statement_block(p):
		'''statement : USE statement_decl_list IN statement_list END
					| USE IN statement_list END
					| USE statement_decl_list IN END
					| USE IN END'''
		if len(p) == 6:
			p[0]=Bloque(p[2],p[4])
		elif len(p) == 5 and p[2] == 'in':
			p[0] = Bloque(None,p[3])
		elif len(p) == 5 and isinstance(p[2],ListasSt_Dcl):
			p[0] = Bloque(p[2],None)
		elif len(p) == 4:
			p[0] = Bloque(None, None)
	
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
		elif len(p)==8:
			p[0]=Asignar_Matriz_Elem(Variable(p[2]) ,p[4] ,p[7] )
	
	# instrucciones de control
	def p_IF(p):
		'''statement : IF expression THEN statement_list ELSE statement_list END
					| IF expression THEN statement_list END
					| IF expression THEN ELSE END
					| IF expression THEN statement_list ELSE END
					| IF expression THEN ELSE statement_list END
					| IF expression THEN END'''
		if len(p) == 8:
			p[0] = instruccion_IF(p[2],p[4],p[6])
		elif (len(p)==6 and isinstance(p[4], ListasSt)) or (len(p)==7 and isinstance(p[4],ListasSt)):
			p[0] = instruccion_IF(p[2],p[4],None)
		elif (len(p)==6 and p[4]=='else') or len(p) == 5:
			p[0] = instruccion_IF(p[2],None,None)
		elif len(p)==7 and p[4] == 'else':
			p[0] = instruccion_IF(p[2],None,p[5])
	
	def p_FOR(p):
		'''statement : FOR ID IN expression DO statement_list END
					| FOR ID IN expression DO END'''
		if len(p) == 8:
			p[0] = instruccion_FOR(Variable(p[2]),p[4],p[6])
		else:
			p[0] = instruccion_FOR(Variable(p[2]),p[4],None)
		
	def p_WHILE(p):
		'''statement : WHILE expression DO statement_list END
					| WHILE expression DO END'''
		if len(p) == 6:
			p[0] = instruccion_WHILE(p[2], p[4])
		else:
			p[0] = instruccion_WHILE(p[2], None)
	
# --------------------------------------------------------------------------
	### AUXILIAR 
	def p_type(p):
		'''type : NUMBER
				| BOOLEAN
				| MATRIX PARENTESISABRE expression COMA expression PARENTESISCIERRA
				| ROW PARENTESISABRE expression PARENTESISCIERRA
				| COL PARENTESISABRE expression PARENTESISCIERRA'''
		if len(p)==2:
			p[0] = Type(p[1],None,None)
		elif len(p)==7:
			p[0] = Type(p[1],p[3],p[5])
		elif len(p)==5 and p[1]=='row':
			p[0] = Type(p[1],None,p[3])
		elif len(p)==5 and p[1]=='col':
			p[0] = Type(p[1],p[3],None)
		
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
					| expression COMA parametros_impresion
					| string COMA parametros_impresion'''
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
	yacc.parse(lexer=lx).check(None)
	return (error)
