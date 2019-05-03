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
    [1, ..., num_comp]


    return None

def find_dist_constraint(examples, program_candidate, components):
    return None


def main():
    return ogis(somefunc)


if __name__ == '__main__':
    main()
