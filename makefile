# Makefile del  Analizador Lexicografico del Lenguaje Trinity
# Creado:26/09/14
# Ult.Mod:26/09/14
# Autores:
# 	Carlo Polisano S. 0910672
#	Alejandro Guevara 0910971
trinity: main
	cp main trinity
	chmod +x trinity
clean:
	rm trinity *.pyc *.out parsetab.py
