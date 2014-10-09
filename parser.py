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

def Sintaxer(lx, tokens, textoPrograma):
	
	precedence = (
		('left', 'SUMA', 'MENOS'),
		('left', 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD')
	)
	### EXPRESIONES 
	def p_expression_t_SUMA(p):
		'expression : expression SUMA expression'
		p[0] = p[1] + p[3]
	
	def p_expression_t_AST(p):
		'expression : expression AST expression'
		p[0] = p[1] * p[3]
	
	def p_expression_t_SLASH(p):
		'expression : expression SLASH expression'
		p[0] = p[1] / p[3]
		
	def p_expression_t_MENOS(p):
		'expression : expression MENOS expression'
		p[0] = p[1] - p[3]
		
	def p_expression_t_DIV(p):
		'expression : expression DIV expression'
		p[0] = int(p[1]) / int(p[3])
		
	def p_expression_t_MOD(p):
		'expression : expression MOD expression'
		p[0] = int(p[1]) % int(p[3])
		
	def p_expression_t_PORCENTAJE(p):
		'expression : expression PORCENTAJE expression'
		p[0] = p[1] % p[3]
		
	# The assign statement
	# ID '=' expression
	name= {}
	def p_statement_assing(p):
		"expression : ID IGUAL expression"
		name[p[1]] = p[3]
		
	def p_expression_t_NUMERO(p):
		"expression : NUMERO"
		p[0] = p[1]
		
	#def p_expression(p):
		#'term : NUMERO'
		#p[0] = Int(p[1])
		
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
	print yacc.parse(textoPrograma,lexer=lx)
	
