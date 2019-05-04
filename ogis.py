import z3
import numpy as np
from components import Components
# OGIS

def ogis(oracle):
    ex_set = {}

    components = Components({'transpose': 0, 'eye_like': 0, 'ones_like': 0, 'multiply': 0, 'add': 0, 'matmul': 0})

    example = np.ones((2,2))

    while example is not None:
        ex_set[example] = oracle(example)

        program_candidate = synthesize(ex_set, components)

        if program_candidate is None:
            pass #change components?


        example = find_dist_constraint(ex_set, program_candidate, components)

def synthesize(examples, components):
    # Assume components is a list of <\vec{I},O,phi>
    num_comp = len(components)
    #[0, ..., num_comp-1]
    pi = [z3.Int(f"pi_{i}") for i in range(num_comp)]
    pi_range = [z3.And(0 <= x, x < num_comp) for x in pi]
    ordering = z3.Distinct(pi)
    for i in range(len(components)):
        f_i_constraints = sum(LLeq())
        ########## thing from whiteboard

        # I_pi_i = A1 | ... | I_pi_i = Am | ( |_{k=0,...n-1} (I_pi_i = Ok and k < pi[i]))

        # LLeq(I_pi_i, A1) or ... or LLeq(I_pi_i, Am) or (I_pi_i = O0 and 0 < pi[i]) or (I_pi_i = O1 and 1 < pi[i]) or (I_pi_i = O2 and 2 < pi[i]) or ... or (I_pi_i = On and n-1 < pi[i])


    return None

def LLeq(l1, l2):
    constraint_lst = [l1[i][j] == l2[i][j] for j in range(len(l1[0])) for i in range(len(l1))]
    return constraint_lst

def find_dist_constraint(examples, program_candidate, components):
    return None


def main():
    return ogis(somefunc)


if __name__ == '__main__':
    main()
