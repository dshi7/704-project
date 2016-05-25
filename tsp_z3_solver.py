from z3 import *
import sys

class TSP_Z3:
    """ class of SMT-based TSP solver """

    def __init__(self, size, filename):

        f = open(filename)
        lines = f.readlines()

        curr_line = 0   # record the line ID

        self._num_pts = int(size)

        self._X = [ [ Int("x_%s_%s" % (j,i)) \
                for i in range(self._num_pts) ] \
                for j in range(self._num_pts) ]
        self._U = [ Int("u_%s" % i) for i in range(self._num_pts) ]

        self._cost_matrix = list()
        for s in range(self._num_pts):
            self._cost_matrix.append( \
                    [int(x) for x in lines[curr_line].split()] )
            curr_line += 1

        self._s = Solver()
        self._o = Optimize()

        self._tour = range(self._num_pts)

    def solveTSP_SMT(self):
        for j in range(self._num_pts):
            for i in range(self._num_pts):
                if j != i:
                    self._s.add(And(self._X[j][i] >=0, self._X[j][i] <= 1))
                else:
                    self._s.add(self._X[j][i] ==0)
        for j in range(self._num_pts):
            self._s.add( \
                    Sum([self._X[j][i] \
                    for i in range(self._num_pts)]) == 1 \
                    )
        for i in range(self._num_pts):
            self._s.add( \
                    Sum([self._X[j][i] \
                    for j in range(self._num_pts)]) == 1 \
                    )
        for j in range(1, self._num_pts):
            for i in range(1, self._num_pts):
                if i == j:
                    continue
                self._s.add( self._U[i] - self._U[j] \
                        + self._num_pts * self._X[i][j] \
                        <= self._num_pts - 1 )
        # print self._s
        while self._s.check() == sat:
            print "SAT"
            solved_model = self._s.model()
            for j in range(self._num_pts):
                for i in range(self._num_pts):
                    m = solved_model.evaluate(self._X[j][i])
                    if m.sexpr() == "1":
                        self._tour[j] = i
            src = 0

            for i in range(self._num_pts-1):
                print "from: ", src, " to: ", self._tour[src]
                src = self._tour[src]

            cost = simplify(Sum([Sum([self._cost_matrix[j][i] * solved_model.evaluate(self._X[j][i]) \
                    for i in range(self._num_pts)]) for j in range(self._num_pts)])).sexpr()
            print "cost: ", cost
            self._s.add(Sum([Sum([self._cost_matrix[j][i] * self._X[j][i] \
                    for i in range(self._num_pts)]) for j in range(self._num_pts)]) < cost)

    def solveTSP_OPT(self):
        for j in range(self._num_pts):
            for i in range(self._num_pts):
                if j != i:
                    self._o.add(And(self._X[j][i] >=0, self._X[j][i] <= 1))
                else:
                    self._o.add(self._X[j][i] ==0)
        for j in range(self._num_pts):
            self._o.add( \
                    Sum([self._X[j][i] for i in range(self._num_pts)]) == 1 \
                    )
        for i in range(self._num_pts):
            self._o.add( \
                    Sum([self._X[j][i] for j in range(self._num_pts)]) == 1 \
                    )
        for j in range(1, self._num_pts):
            for i in range(1, self._num_pts):
                if i == j:
                    continue
                self._o.add( self._U[i] - self._U[j] + self._num_pts * self._X[i][j] <= self._num_pts - 1 )
        self._o.minimize(Sum([Sum([self._cost_matrix[j][i] * self._X[j][i] \
                for i in range(self._num_pts)]) for j in range(self._num_pts)]) )
        if self._o.check()==sat:
            solved_model = self._o.model()
            for j in range(self._num_pts):
                for i in range(self._num_pts):
                    m = solved_model.evaluate(self._X[j][i])
                    if m.sexpr() == "1":
                        self._tour[j] = i
            src = 0

            for i in range(self._num_pts-1):
                print "from: ", src, " to: ", self._tour[src]
                src = self._tour[src]
            cost = simplify(Sum([Sum([self._cost_matrix[j][i] * solved_model.evaluate(self._X[j][i]) \
                    for i in range(self._num_pts)]) for j in range(self._num_pts)])).sexpr()
            print "cost: ", cost

