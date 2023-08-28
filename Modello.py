from mip import *
from sys import stdout
import contextlib

m = Model()
m.store_search_progress_log=True

file = open("Test_3/rec_24_24.txt")
riga=file.readline()
righe = int(riga)
colonna=file.readline()
colonne=int(colonna)

grid = [file.readline().split(',') for j in range(righe)]
class Rettangolo:
    altezza=int
    larghezza=int
    costo=int
    def stampa(self):
        return self.altezza, self.larghezza, self.costo
    def __init__(self, attributi):
        self.altezza=int(attributi[0])
        self.larghezza=int(attributi[1])
        self.costo=int(attributi[2])

rettangoli=int(file.readline())
R={'rettangolo_%d'%(j+1):Rettangolo(file.readline().split(',')) for j in range(rettangoli)}


x={(i,j,r):m.add_var(name='x(%d,%d,%s)'%(i,j,r), var_type=BINARY) for r in R for i in range(righe) for j in range(colonne) if i<=(righe-R[r].altezza+1) and j<=(colonne-R[r].larghezza+1)}
for r in R:
    m+=xsum(x[i,j,r] for i in range(righe-R[r].altezza+1) for j in range(colonne-R[r].larghezza+1))<=1, 'vincolo_'+r

y={(i,j):m.add_var(name='y(%d,%d)'%(i,j), var_type=BINARY) for i in range(righe) for j in range(colonne)}
for i in range(righe):
    for j in range(colonne):
        if int(grid[i][j])>0:
            m+=y[i,j]<=xsum(xsum(x[q,s,r] for q in range(righe-R[r].altezza+1) for s in range(colonne-R[r].larghezza+1) if q>(i-R[r].altezza) and q<=i and s>(j-R[r].larghezza) and s<=j) for r in R), 'vincolo_per_y(%d,%d)'%(i,j)
cardR=len(R)
for i in range(righe):
    for j in range(colonne):
        if int(grid[i][j])<0:
            m+=cardR*y[i,j]>=xsum(xsum(x[q,s,r] for q in range(righe-R[r].altezza+1) for s in range(colonne-R[r].larghezza+1) if q>(i-R[r].altezza) and q<=i and s>(j-R[r].larghezza) and s<=j) for r in R ), 'vincolo_per_y(%d,%d)'%(i,j)
m.objective=maximize(xsum(xsum(int(grid[i][j])*y[i,j] for i in range(righe)) for j in range(colonne))-xsum(xsum(R[r].costo*x[i,j,r] for i in range(righe-R[r].altezza+1) for j in range(colonne-R[r].larghezza+1)) for r in R))

m.optimize(max_seconds=300)
print(m.search_progress_log.log)


m.write('model.lp')
for r in R:
    for i in range(righe-R[r].altezza+1):
        for j in range(colonne-R[r].larghezza+1):
            if x[i,j,r].x>0.99:
                print('x(%d,%d,%s)'%(i,j,r))
print(m.objective_value)
