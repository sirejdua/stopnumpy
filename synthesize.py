from z3 import *

class Formulate:
    def __init__(self, examples, components):
        self.E = examples # guaranteed size > 0
        self.P, self.R, phi_i = zip(*components)
        self.phi_lib = And(*[phi_i])
        self.N = len(components) # number of components
        self.len_I = len(examples[0][0]) # number of formal parameters
        self.M = self.len_I + self.N
        self.L = # TODO: fill in

    def psi_cons(self):
        # return And(*[self.L[x] != self.L[y] for x in self.R for y in self.R if x != y])
        return Distinct(*[self.L[x] for x in self.R])

    def psi_acyc(self):
        return And(*[And(*[self.L[x] <= self.L[self.R[i]] for x in self.P[i]]) for i in range(self.N)])

    def psi_wfp(self):
        return  And(And(*[And(0 <= self.L[x], self.L[x] < self.M) for x in self.P]),
                    And(*[And(self.len_I <= self.L[x], self.L[x] < self.M) for x in self.R]),
                    self.psi_cons(),
                    self.psi_acyc())

    def psi_conn(self, I, O):
        all_x_y = self.P + self.R + I + [O]
        return And(*[Implies(self.L[x] == self.L[y], x == y) for x in all_x_y for y in all_x_y])

    def phi_func(self, I, O):
        return And(self.psi_wfp(), 
                   self.phi_lib, 
                   self.psi_conn(I, O))

    def Behave_E(self):
        return And(*[self.phi_func(a, b) for a, b in self.E])


def test():
    synthesize()

if __name__ == '__main__':
    test()
