import sys
import pandas as pd
import time, numpy as np
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Parameters
S = np.array([150, 20, 130]) # S_i

Total_Supply = sum(S)

d = np.array([135, 75, 45, 45]) # d_j

Total_Demand = sum(d)

Feasibility_Condition = (Total_Demand <= Total_Supply) # Check on Feasibility Condition

c = np.array([[5, 2, 3, 9],
             [7, 1, 12, 4],
             [8, 15, 19, 2]]) # c_ij 

m = len(c) # Number of Suppliers
n = len(c[0]) # Number of Demand Centers

range_i = range(0,m)
range_j = range(0,n)

#Create Model
model = pyo.ConcreteModel()

#Define variables
model.x = pyo.Var(range(m), # index i
                  range(n), # index j
                 # within=Integers,# In this problem you can also assume that variables xij take on integer values (and
                                   # non-negative ones), it depends on the good you are dealing with.
                  bounds = (0,None))
x = model.x

#Define Constraints 
model.C1 = pyo.ConstraintList() 
for i in range_i:
    model.C1.add(expr = sum(x[i,j] for j in range_j)  <= S[i])

model.C2 = pyo.ConstraintList() 
for j in range_j:
    model.C2.add(expr = sum(x[i,j] for i in range_i) == d[j])
    
# Define Objective Function
model.obj = pyo.Objective(expr = sum(x[i,j]*c[i][j] for i in range_i for j in range_j), 
                          sense = minimize)
    
begin = time.time()
opt = SolverFactory('cplex')
results = opt.solve(model)

deltaT = time.time() - begin # Compute Exection Duration

model.pprint()

sys.stdout = open("Transportation_Problem_Results.txt", "w") #Print Results on a .txt file

print('Time =', np.round(deltaT,2))

if Feasibility_Condition == True: # if feasibility conditon holds
    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):

        print('Total Cost (Obj value) =', pyo.value(model.obj))
        print('Solver Status is =', results.solver.status)
        print('Termination Condition is =', results.solver.termination_condition)
        print(" " )
        for i in range_i:
            print("From Supply Center " , i+1)
            for j in range_j:
                
                if pyo.value(x[i,j]) != 0:
                      print("---->to demand center " , j+1 , " flows " ,pyo.value(x[i,j]) , " and related cost is = " , pyo.value(x[i,j])*c[i][j])
            print(' ')              
    elif (results.solver.termination_condition == TerminationCondition.infeasible):
       print('Model is unfeasible')
      #print('Solver Status is =', results.solver.status)
       print('Termination Condition is =', results.solver.termination_condition)
    else:
        # Something else is wrong
        print ('Solver Status: ',  result.solver.status)
        print('Termination Condition is =', results.solver.termination_condition)
else:
    print('Feasibility Condition does not hold, total demand is ', Total_Demand, 'and Total Supply is ', Total_Supply)
    
sys.stdout.close()