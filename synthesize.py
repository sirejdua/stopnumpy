from z3 import *
import itertools
from components import Components
from examples.transpose import *

class Formulate:
    # examples: list of (input, output) ndarray tuples with same size
    # components: list of (i, o, phi(i,o)) triples as specified in components.py
    def __init__(self, examples, components, prefix=""):
        self.examples = examples
        self.components = components
        self.prefix = prefix
        self.E = [(self.convert(i), self.convert(o)) for i,o in examples]

        self.I_i, self.R, phi_i = zip(*components)
        self.P = list(itertools.chain(*self.I_i)) # union of vectors
        self.phi_lib = And(*phi_i)

        self.len_I = 1 # number of formal parameters
        self.N = len(components) # number of components
        self.M = self.len_I + self.N
        
        # maps each component input and output and formal params and output to a symbolic int
        all_locs = list(itertools.chain(self.P, self.R))
        self.L = {i: Int(f"{self.prefix}L_{l}") for i, l in zip(all_locs, range(len(all_locs)))}

        self.sym_I = "T_FA"
        self.L[self.sym_I] = 0
        self.sym_O = "T_O"
        self.L[self.sym_O] = self.M - 1

    def convert(self, arr):
        return tuple(tuple(i.tolist()) for i in arr)

    def synthesize(self):
        s = Solver()
        s.add(self.Behave_E())
        print(s)
        s.check()
        return s.model()

    def Lval2Prog(self, model, components):
        if model == None:
            print("UNSAT")
            return None

        print(model)
        print()

        funcs = [None for i in range(1 + self.N)] # assuming 1 formal parameter
        args = [None for i in range(1 + self.N)]

        for I_j, O_j, j in zip(self.I_i, self.R, range(len(self.R))):
            i = model[self.L[O_j]].as_long()
            funcs[i] = j
            args[i] = [model[self.L[I_j_k]].as_long() for I_j_k in I_j]

        func_names = ['input'] + components.get_names_from_indices(funcs[1:])

        for i in range(1 + self.N):
            if args[i] == None:
                print(f"l{i} = {func_names[i]}")
            elif len(args[i]) == 1:
                print(f"l{i} = {func_names[i]}(l{args[i][0]})")
            elif len(args[i]) == 2:
                print(f"l{i} = {func_names[i]}(l{args[i][0]}, l{args[i][1]})")
            else:
                print("TODO: pretty printing support for larger arg lists")

        return zip(funcs, args)

    def dist_constraint(self):

        I = tuple( tuple(z3.Int(f"IDC_{i}_{j}") for i in range(len(self.E[0][0]))) for j in range(len(self.E[0][0][0])))
        O1 = tuple( tuple(z3.Int(f"ODC1_{i}_{j}") for i in range(len(self.E[0][1]))) for j in range(len(self.E[0][1][0])))
        O2 = tuple( tuple(z3.Int(f"ODC2_{i}_{j}") for i in range(len(self.E[0][1]))) for j in range(len(self.E[0][1][0])))

        F2 = Formulate(self.examples, self.components, "F2_")
        return I, And(self.Behave_E(), F2.Behave_E(), self.phi_func(I, O1), F2.phi_func(I, O2), Not(self.LLeq(O1, O2)))

    def psi_cons(self):
        # return And(*[self.L[x] != self.L[y] for x in self.R for y in self.R if x != y])
        return Distinct(*[self.L[x] for x in self.R])

    def psi_acyc(self):
        return And(*[And(*[self.L[x] < self.L[self.R[i]] for x in self.I_i[i]]) for i in range(self.N)])

    def psi_wfp(self):
        return  And(And(*[And(0 <= self.L[x], self.L[x] < self.M) for x in self.P]),
                    And(*[And(self.len_I <= self.L[x], self.L[x] < self.M) for x in self.R]),
                    self.psi_cons(),
                    self.psi_acyc())

    def psi_conn(self, I, O):
        # sym_I = [f"LFA_{i}" for i in range(len(I))]

        all_x_y = self.P + list(self.R) + [self.sym_I, self.sym_O]
        return And(*[Implies(self.L[x] == self.L[y], self.EQ(x,y,I,O)) for x in all_x_y for y in all_x_y if x != y])


    def EQ(self, x, y, I, O):
        if x == self.sym_I:
            x = I
        elif x == self.sym_O:
            x = O

        if y == self.sym_I:
            y = I
        elif y == self.sym_O:
            y = O

        return self.LLeq(x, y)

    def LLeq(self, l1, l2):
        constraint_lst = [l1[i][j] == l2[i][j] for j in range(len(l1[0])) for i in range(len(l1))]
        return And(*constraint_lst)


    def phi_func(self, I, O):
        return And(self.psi_wfp(), 
                   self.phi_lib, 
                   self.psi_conn(I, O))

    def Behave_E(self):
        return And(*[self.phi_func(a, b) for a, b in self.E])


def test():
    import numpy as np

    oracle = lambda x: x.T
    oracle = transpose3

    ex_set = []
    example = np.array([[1, 2], [1, 2]])

    # TODO: to add more than one formal parameter make sure to make first element of tuple a list
    ex_set.append((example, oracle(example)))  
    input_shape = example.shape

    components = Components({'transpose': 1, 'eye_like': 1, 'ones_like': 0, 'multiply': 0, 'add': 0, 'matmul': 0}, input_shape)

    f = Formulate(ex_set, components.get_list())
    model = f.synthesize()
    f.Lval2Prog(model, components)

if __name__ == '__main__':
    test()
