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

class Expresion(object):
    def __init__(self, hijos):
      self.hijos = hijos

    def show(self, depth):
      return (
        '\n' + '  '*depth + self.__class__.__name__ + ':'
        + ''.join(
          ['\n' + '  '*(depth+1) + x + ': ' + (y.show(depth + 2) if isinstance(y, Expresion) else str(y)) for (x, y) in self.hijos.items()]
        )
      )

class Suma(Expresion):
	def __init__(self, p):
		self.hijos = {'operando izquierdo': p[1], 'operando derecho': p[3]}

# LITERALES!
class LiteralNumerico(Expresion): pass
class Booleano(Expresion): pass
class Variable(Expresion): pass

class Asignar(Expresion):
	def __init__(self,variable,expresion):
		self.hijos = {'variable': variable, 'expresion': expresion}
		
def Sintaxer(lx, tokens, textoPrograma):
	
	precedence = (
		('left', 'SUMA', 'MENOS'),
		('left', 'AST','SLASH','PORCENTAJE', 'DIV', 'MOD')
	)
	
	# The assign statement
	# ID '=' expression
	#name= {}
	
	def p_statement_assing(p):
		"expression : ID IGUAL expression"
		p[0] = Asignar(Variable(p[1]),p[3])
	
	### EXPRESIONES 
	def p_expression_SUMA(p):
		'expression : expression SUMA expression'
		p[0] = Suma(p)
	
	#def p_expression_t_AS(p):
		#'expression : expression AST expression'
		#p[0] = p[1] * p[3]
	
	#def p_expression_t_SLASH(p):
		#'expression : expression SLASH expression'
		#p[0] = p[1] / p[3]
		
	#def p_expression_t_MENOS(p):
		#'expression : expression MENOS expression'
		#p[0] = p[1] - p[3]
		
	#def p_expression_t_DIV(p):
		#'expression : expression DIV expression'
		#p[0] = int(p[1]) / int(p[3])
		
	#def p_expression_t_MOD(p):
		#'expression : expression MOD expression'
		#p[0] = int(p[1]) % int(p[3])
		
	#def p_expression_t_PORCENTAJE(p):
		#'expression : expression PORCENTAJE expression'
		#p[0] = p[1] % p[3]
		
	##  ## REDUCE ## LITERALES ## ##
	def p_expression_NUMERO(p):
		"expression : NUMERO"
		p[0] = LiteralNumerico({'valor': int(p[1]) } )
		
	def p_expression_ID(p):
		"expression : ID"
		p[0] = Variable({'Variable': str(p[1])})
			
	#def p_expression_BOOLEAN(p):
		#"""expression : FALSE
					#| TRUE"""
		#p[0] = Booleano({'valor': str(p[1])})
			
			
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
	print yacc.parse(lexer=lx, debug=1).show(0)
	
