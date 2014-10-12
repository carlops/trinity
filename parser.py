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

class Program:
	def __init__(self,cuerpo)
		self.cuerpo=cuerpo
	

class Expresion(object):
	def __init__(self, hijos):
		self.hijos = hijos

	def show(self, depth):
		print('  '*depth + self.name + ':')
		for i in self.hijos:
			self.hijos[i].show(depth+1)
	
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
	
class Variable(Expresion): 
	def __init__(self,valor):
		self.valor = valor
	def show(self, depth):
		print('  '*depth + 'Variable:\n'+'  '*(depth+1) + 'nombre: '+str(self.valor))
	

def Sintaxer(lx, tokens, textoPrograma):
	
	precedence = (
		("left", 'OR'),
		("left", 'AND'),
		('left', 'SUMA', 'MENOS'),
		('left', 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD')
	)
	
	def p_program(p):
		"program : PROGRAM statement"
		p[0] = Program(p[2])
	
	### STATEMENTS
	def p_statement_assing(p):
		"expression : ID IGUAL expression"
		p[0] = Asignar(Variable(p[1]),p[3])
	
	### EXPRESIONES 
	def p_expression_SUMA(p):
		'expression : expression SUMA expression'
		p[0] = OperacionBinaria(p,'Suma')
	
	def p_expression_AST(p):
		'expression : expression AST expression'
		p[0] = OperacionBinaria(p,'Multiplicacion')
	
	def p_expression_t_SLASH(p):
		'expression : expression SLASH expression'
		p[0] = OperacionBinaria(p,'Division')
		
	def p_expression_t_MENOS(p):
		'expression : expression MENOS expression'
		p[0] = OperacionBinaria(p,'Resta')
		
	def p_expression_t_PORCENTAJE(p):
		'expression : expression PORCENTAJE expression'
		p[0] = OperacionBinaria(p,'Modulo')
		
	def p_expression_t_DIV(p):
		'expression : expression DIV expression'
		p[0] = OperacionBinaria(p,'Division Entera')
		
	def p_expression_t_MOD(p):
		'expression : expression MOD expression'
		p[0] = OperacionBinaria(p,'Modulo Entero')
		
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
		
	def p_expression_Comparativos(p):
		"""expression : expression IGUAL2 expression
					| expression DISTINTO expression
					| expression MAYORIGUAL expression
					| expression MENORIGUAL expression
					| expression MAYORQUE expression
					| expression MENORQUE expression"""
		p[0] = OperacionBinaria(p,str(p[2]))
		
	def p_error(p):
		print ("Error: {} de tipo {} encontrado en {},{}".format(p.value,p.type,p.lineno,p.lexpos))
		print("ERROR")
		
	# Precedence defined for expressions
	#precedence = (
		#("left", 'SUMA', 'MENOS'),
		#("left", 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD')
	#)
		## bool
		#("left", 'OR'),
		#("left", 'AND'),
		#("right", 'NOT'),
		# ("left", 'EQUIVALENT', 'INEQUIVALENT'),
		## compare
		#("nonassoc", 'BELONG'),
		#("nonassoc", 'EQUAL', 'UNEQUAL'),
		#("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
		## range
		#("left", 'INTERSECTION'),
		## ("left", 'UNION'),
		## ("nonassoc", 'MAPTIMES'),
		## int
		## AQUI
		## range
		#("nonassoc", 'FROMTO'),
		## int
		#("right", 'UMINUS'),
	#)
	
	yacc.yacc()
	
	#print yacc.parse(lexer=lx)
	print yacc.parse(lexer=lx).show(0)

