from z3 import *
import sys

class SolverDB:
    """ class of SMT-based ILP Solver """

    def __init__(self, filename):
        f = open(filename)
        lines = f.readlines()

        curr_line = 0

        #   read number of rows and number of columns in 1st line
        dim = lines[curr_line].split()
        curr_line += 1

        self._num_rows = int(dim[0])
        self._num_cols = int(dim[1])

        print "# Variables   = ", self._num_cols
        print "# Constraints = ", self._num_rows

        #   define primal variables
        self._primal_vars = [ Int("x_%s" % i) for i in range(self._num_cols) ]

        #   define linear objective function
        self._obj_func = [float(x) for x in lines[curr_line].split()]
        print "Objective Function: ", self._obj_func
        curr_line += 1

        #   define constraints
        self._constraints = list()
        for r in range(0, self._num_rows):
            self._constraints.append([float(x) for x in lines[curr_line].split()])
            curr_line += 1

        #   define the RHS of rows
        self._rhs_rows = [float(x) for x in lines[curr_line].split()]
        curr_line += 1

        #   define the types of rows
        self._types = lines[curr_line].split()
        curr_line += 1

        #   define the tuple <M,ub,ob> of solver
        self._model_set = list()
        self._ub = sys.float_info.min
        self._ob = sys.float_info.max
        self._ub = -100
        self._ob = 100

        #   print the state tuple
        print "Model Set: ", self._model_set
        print "Under-approximation: ", self._ub
        print "Over-approximation:  ", self._ob

    def init_solver(self):
        self._s = Solver()
        for row in range(0, self._num_rows):
            if self._types[row] == 'L':
                self._s.add( Sum([self._constraints[row][c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) <= self._rhs_rows[row] )
            elif self._types[row] == 'E':
                self._s.add( Sum([self._constraints[row][c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) == self._rhs_rows[row] )
            else:
                self._s.add( Sum([self._constraints[row][c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) >= self._rhs_rows[row] )
        print self._s

    def global_push(self):
        self._s.push()
        self._s.add( Sum([self._obj_func[c] * self._primal_vars[c] \
                for c in range(0, self._num_cols)]) >= self._ub )
        if self._s.check() == sat:
            self._model_set.append( self._s.model() )
            print "Global Push: ", self._model_set[-1]
            print "Updated Obj: ", simplify( Sum([self._obj_func[c] * self._model_set[-1][self._primal_vars[c]] \
                    for c in range(0, self._num_cols)]) )
        self._s.pop()

    def unbounded(self):
        if not self._model_set:
            return  #   return if the model set is empty
        temp_m = self._model_set[-1]
        temp_s = Solver()
        temp_eq = list()

        for row in range(0, self._num_rows):
            lhs = sum(self._constraints[row][c] * self._primal_vars[c] \
                    for c in range(0, self._num_cols))
            rhs = self._rhs_rows[row]
            print lhs, " ", rhs
            print type(lhs)
            print type(rhs)

            if lhs > 1:
                print "yes"
            else:
                print "no"

        temp_s.add( \
                Sum([self._obj_func[c] * temp_m[self._primal_vars[c]] \
                for c in range(0, self._num_cols)]) < \
                simplify(Sum([self._obj_func[c] * self._primal_vars[c] \
                for c in range(0, self._num_cols)])) )

        print temp_eq

        print temp_s
        if temp_s.check() == unsat:
            return
        p2 = temp_s.model()
        print p2
        print "Updated Obj: ", simplify( Sum([self._obj_func[c] * p2[self._primal_vars[c]] \
                for c in range(0, self._num_cols)]) )

    def solve_linear_program(self):
        self.global_push()
        self.unbounded()

    def solve_integer_program(self):
        step_count = 1
        while self._s.check() == sat:
            print "Round ", step_count
            sol = self._s.model()
            print "satisfiable solution: ", sol
            print "obj coefficents: ", self._obj_func
            updated_obj = 0
            self._s.add( \
                    Sum([self._obj_func[c] * self._primal_vars[c] \
                    for c in range(0, self._num_cols)]) \
                    > Sum([self._obj_func[c] * sol[self._primal_vars[c]] \
                    for c in range(0, self._num_cols)]) )
            print self._s
            step_count += 1
