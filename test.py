import sys
from z3 import *
from my_solver import *
from my_tsp_solver import *

if len(sys.argv) == 1:
    print "Error: input file needs to specify"
else:
    print "Input file: ", str(sys.argv[1])
    my_solver = TSP(str(sys.argv[1]))
    my_solver.solveTSP()

