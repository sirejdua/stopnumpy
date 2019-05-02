import z3
import numpy as np

# OGIS

def ogis(oracle):
    ex_set = {}

    components = {'transpose': 0, 'eye-like': 0, 'ones-like': 0, 'multiply': 0, 'add': 0}

    example = np.ones((2,2))

    while example is not None:
        ex_set[example] = oracle(example)

        program_candidate = synthesize(ex_set, components)

        if program_candidate is None:
            #change components?
            pass


        example = find_dist_constraint(ex_set, program_candidate, components)


def synthesize(examples, components):
    return None

def find_dist_constraint(examples, program_candidate, components):
    return None


def main():
    return ogis(somefunc)


if __name__ == '__main__':
    main()
