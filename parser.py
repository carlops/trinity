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

def Sintaxer(tokens):
	
### EXPRESIONES 
	def p_expression_TknSUMA(p):
		'expression : expression TknSUMA term'
		p[0] = p[1] + p[3]
	
	def p_expression_TknAST(p):
		'expression : expression TknAST term'
		p[0] = p[1] * p[3]
	
	def p_expression_TknNUMERO(p):
		"expression : TknNUMERO"
		p[0] = Int(p[1])
		
	def p_term(p):
		'term : TknNUMERO'
		p[0] = Int(p[1])
		
	# The assign statement
	# ID '=' expression
	def p_statement_assing(p):
		"expression : ID TknIGUAL expression"
		p[0] = p[1]
		
	def p_error(p):
		print ("Error" + p)
	
	yacc.yacc()
