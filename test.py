import sys
import time
from z3 import *
from tsp_z3_solver import *

if len(sys.argv) < 3:
    print "Error: input file needs to specify"
else:
    print "Problem Size: ", str(sys.argv[1])
    print "Input file: ", str(sys.argv[2])

    my_solver = TSP_Z3(str(sys.argv[1]), str(sys.argv[2]))

    begin_time = time.time()
    my_solver.solveTSP_SMT()
    elapsed_time = time.time() - begin_time
    print "Elapsed Time (seconds): ", elapsed_time

    begin_time = time.time()
    my_solver.solveTSP_OPT()
    elapsed_time = time.time() - begin_time
    print "Elapsed Time (seconds): ", elapsed_time

