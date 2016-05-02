from z3 import *

class SolverDB:
    """ class of SMT-based ILP Solver """

    def __init__(self, filename):
        f = open(filename)
        lines = f.readlines()

        curr_line = 0

        #   read number of rows and number of columns in 1st line
        dim = lines[curr_line].split()
        curr_line += 1

        self._num_rows = 3
        self._num_cols = 5

        #   define primal variables
        self._primal_vars = RealVector('x', self._num_cols)

        #   define linear objective function
        self._obj_func = lines[curr_line].split()
        curr_line += 1

        #   define constraints
        self._constraints = list()
        for r in range(0, self._num_rows):
            self._constraints.append(lines[curr_line].split())
            curr_line += 1

        #   define the RHS of rows
        self._rhs_rows = lines[curr_line].split()
        curr_line += 1

        #   define the types of rows
        self._types = lines[curr_line].split()
        curr_line += 1

        #   define the tuple <M,ub,ob> of solver
        self._model_set = list()
        self._ub = -float("inf")
        self._ob = float("inf")

        #print _s

    def init_solver(self):
        self._s = Solver()
        for row in range(0, self._num_rows):
            if self._types[row] == 'L':
                self._s.add( Sum([self._obj_func[c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) <= self._rhs_rows[row] )
            elif self._types[row] == 'E':
                self._s.add( Sum([self._obj_func[c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) == self._rhs_rows[row] )
            else:
                self._s.add( Sum([self._obj_func[c] * self._primal_vars[c] \
                        for c in range(0, self._num_cols)]) >= self._rhs_rows[row] )
        print self._s
        print "hello world!"

        if self._s.check() == sat:
            print self._s.model()

