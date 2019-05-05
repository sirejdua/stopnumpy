import z3
import numpy as np
from components import Components
# OGIS

def ogis(oracle):
    ex_set = []

    components = Components({'transpose': 0, 'eye_like': 0, 'ones_like': 0, 'multiply': 0, 'add': 0, 'matmul': 0})

    example = np.ones((2,2))

    while example is not None:
        ex_set.append((example, oracle(example)))

        program_candidate = synthesize(ex_set, components)

        if program_candidate is None:
            pass #change components?


        example = find_dist_constraint(ex_set, program_candidate, components)

def synthesize(examples, components):
    # ask z3 to find the valid model
    s = z3.Solver()
    s.add(valid_program_constraint(examples, components))
    num_comp = len(components)
    if (s.check() == sat):
        m = s.model()
        r = [ [ m.evaluate(z3.Int(f"pi_{i}")) for i in range(num_comp)]]
        print(r)
    return r

def valid_program_constraint(examples, components):
    # Assume components is a list of <\vec{I},O,phi>
    num_comp = len(components)
    shape = examples[0][0].shape
    #[0, ..., num_comp-1]
    pi = [z3.Int(f"pi_{i}") for i in range(num_comp)]
    pi_range = [z3.And(0 <= x, x < num_comp) for x in pi]
    ordering = z3.Distinct(pi)
    arg = [[z3.Int(f"arg_{i}_{j}") for i in range(shape[0])] for j in range(shape[1])]
    constraints = []
    for i in range(num_comp):
        Ivec, O, phi = components[i]
        for I_pi_i in Ivec:
            arg_constraint = LLeq(I_pi_i, arg)
            o_constraints = z3.Or(*[LLeq(I_pi_i, components[j][1]) + [j < pi[i]] for j in range(num_comp)])
            constraints.append(z3.Or(arg_constraint, o_constraints))
        ########## thing from whiteboard

        # I_pi_i = A1 | ... | I_pi_i = Am | ( |_{k=0,...n-1} (I_pi_i = Ok and k < pi[i]))

        # LLeq(I_pi_i, A1) or ... or LLeq(I_pi_i, Am) or (I_pi_i = O0 and 0 < pi[i]) or (I_pi_i = O1 and 1 < pi[i]) or (I_pi_i = O2 and 2 < pi[i]) or ... or (I_pi_i = On and n-1 < pi[i])

    # + means list concat
    output = [[z3.Int(f"output_{i}_{j}") for i in range(shape[0])] for j in range(shape[1])]
    output_of_last_is_function_output = z3.Or(*[LLeq(fn_output, components[j][1]) + [j == pi[n-1]] for j in range(num_comp)])

    all_constraints = pi_range + ordering + constraints + [output_of_last_is_function_output]
    return all_constraints

def LLeq(l1, l2):
    constraint_lst = [l1[i][j] == l2[i][j] for j in range(len(l1[0])) for i in range(len(l1))]
    return constraint_lst

def find_dist_constraint(examples, program_candidate, components):
    return None


def main():
    # return ogis(somefunc)
    return test_synthesize()


def test_synthesize():
    oracle = lambda x: x.T

    ex_set = []
    example = np.array([1,2,3,4]).reshape((2,2))
    ex_set.append((example, oracle(example)))

    input_shape = example.shape

    components = Components({'transpose': 1, 'eye_like': 0, 'ones_like': 0, 'multiply': 0, 'add': 0, 'matmul': 0}, input_shape).get_list()

    program = synthesize(ex_set, components)


if __name__ == '__main__':
    main()
