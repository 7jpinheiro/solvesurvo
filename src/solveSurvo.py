# -*- coding: cp1252 -*-

import sys
sys.path

from z3 import *

print "\n*** solveSurvo ***\n"

if len(sys.argv)<2:
    print "Falta ficheiro de input"
    print "solveSurvo.py <ficheiro input>"
    sys.exit()

filename = sys.argv[1]

f = open(filename,"r") 

cx = f.readline().split()
cy = f.readline().split()

cx = [int(a) for a in cx]
cy = [int(a) for a in cy]

print "Total a somar em y:" ,cy
print "Total a somar em x:",cx

array = []

for line in f:
    array.append( line.split() )

array = [map(int,x) for x in array]
f.close()
print "\nPontos recebidos:\n", array

cx_size = len(cx)
cy_size = len(cy)


#Criação do tabuleiro inicial do jogo
table =[ [ 0 for i in range(cx_size) ] for j in range(cy_size) ]
for s in array:
    table[s[0]-1][s[1]-1] = s[2]      


print "\nTabuleiro inicial de jogo:\n"
for l in table:
    print l

print "\nLinhas   :" , cy
print "Colunas  :" , cx
#Criação de uma tabela com variaveis de cx_size x cy_size

X = [ [ Int("x_%s_%s" % (i+1, j+1)) for i in range(cx_size) ] 
      for j in range(cy_size) ]

#Constraints
#Cada celula tem valores entre 1...cx*cy (inteiros)
celulas  = [ And(1 <= X[j][i], X[j][i] <= cx_size*cy_size) for i in range(cx_size) for j in range(cy_size) ]

#Cada número é unico na matriz
num_unico =  [ Distinct(X[j][i]) for i in range(cx_size) for j in range(cy_size) ]


#O somatorio das linhas tem de ser igual ao numero em cx
som_x = [ cy[i] == sum(X[i]) for i in range(cy_size) ]

#O somatorio das colunas tem de ser igual ao numero em cy
som_y   = [ cx[j] == sum([ X[i][j] for i in range(cy_size) ])
             for j in range(cx_size) ]

#Constraints juntas
solveSurvo = celulas + num_unico + som_x + som_y

instancia = [ If(table[i][j] == 0, 
                  True, 
                  X[i][j] == table[i][j]) 
               for i in range(cy_size) for j in range(cx_size) ]

s = Solver()
s.add(solveSurvo + instancia)
print "\nSolucao:\n"
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(cx_size) ] 
          for i in range(cy_size) ]
    for l in r:
        print l
    nf = open('result_' + filename  ,'w+')
    for line in r:
        nf.write("%s\n" %line)
    nf.write("\nLinhas   : %s\n" % cy)
    nf.write("Colunas  : %s\n" % cx)    
    nf.close()
else:
    print "\nimpossivel resolver\n"

