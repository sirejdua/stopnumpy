import z3
import numpy as np
from components import Components
from  synthesize import Formulate
import pdb
# OGIS

def ogis(oracle):
    ex_set = []
    ishape = (2,2)

    components = Components({'transpose': 0, 'eye_like': 1, 'ones_like': 0, 'multiply': 0, 'add': 1, 'matmul': 0}, ishape)
    ex_set.append((np.ones((2,2)), oracle(np.ones((2,2)))))

    example = np.eye(ishape[0])

    program_candidate = None

    while example is not None:
        ex_set.append((example, oracle(example)))

        f = Formulate(ex_set, components.get_list())
        satisfying_constraints = f.Behave_E()
        s = z3.Solver()
        s.add(satisfying_constraints)
        if (s.check() == z3.sat):
            I, unique_constraints = f.dist_constraint()
            s2 = z3.Solver()
            s2.add(unique_constraints)
            if (s2.check() == z3.sat):
                print("nonunique; getting new example")
                model = s2.model()
                example = np.array([[model.evaluate(i) for i in il] for il in I])
            else:
                print("unsat")
                #done
                program_candidate = f.Lval2Prog(s.model(), components)
                break
        else:
            print("No valid program candidate found")
            return False
    return program_candidate


def synthesize(examples, components):
    # ask z3 to find the valid model
    s = z3.Solver()
    s.add(valid_program_constraint(examples, components))
    # Add in the phi constraint
    s.add(valid_on_examples(examples, components))
    pdb.set_trace()

    if (s.check() == z3.sat):
        # This code is for interpreting a model into a program
        # maybe this can move to a helper since it can be used in other places
        m = s.model()
        return interpret_model(m, examples, components)
    else:
        print("NOT SAT")
        return False

def interpret_model(model, examples, components):
    num_comp = len(components)
    shape = examples[0][0].shape
    r = [model.evaluate(z3.Int(f"pi_{i}")) for i in range(num_comp)]
    arg = [[model.evaluate(z3.Int(f"arg_{i}_{j}")) for i in range(shape[0])] for j in range(shape[1])]
    inputs = [ [ [[ model.evaluate(v) for v in irow] for irow in I]  for I in Ivec]    for Ivec,_,_ in components]
    outputs = [ [ [ model.evaluate(v) for v in orow] for orow in O]    for _,O,_ in components]

    #Link each input to one of the outputs
    prog = []
    for i in range(num_comp):
        args = []
        for in_eval in inputs[r[i].as_long()]:
            input_to_component = None
            if all(self.LLeq(in_eval, arg)):
                input_to_component = "arg"
            else:
                for j in range(r[i].as_long()):
                    if all(LLeq(in_eval, outputs[j])):
                        input_to_component = f"output{j}"
                        break
            args.append(input_to_component)
        prog.append((r[i], args))
    return prog

def valid_on_examples(examples, components):
    # do something with phi 
    shape = examples[0][0].shape
    example_constraints = []
    for i,o in examples:
        pdb.set_trace()
        i = [x.tolist() for x in i]
        o = [x.tolist() for x in o]
        arg = [[z3.Int(f"arg_{i}_{j}") for i in range(shape[0])] for j in range(shape[1])]
        ieq = z3.And(*LLeq(i, arg))
        oeq = z3.And(*LLeq(o, components[-1][1]))
        example_constraints.append(z3.Implies(ieq, oeq))
    return example_constraints

def valid_program_constraint(examples, components):
    # Assume components is a list of <\vec{I},O,phi>
    num_comp = len(components)
    shape = examples[0][0].shape
    #[0, ..., num_comp-1]
    pi = [z3.Int(f"pi_{i}") for i in range(num_comp)]
    pi_range = [z3.And(0 <= x, x < num_comp) for x in pi]
    ordering = z3.Distinct(pi)
    #arg = [[z3.Int(f"arg_{i}_{j}") for i in range(shape[0])] for j in range(shape[1])]
    num_args = 1
    arg = z3.Int(f"L_0")
    locations = [z3.Int(f"L_{i}") for i in range(num_comp + num_args)]
    constraints = []
    loc_constraints = []

    for i in range(num_comp):
        Ivec, O, phi = components[i]
        for j in range(len(Ivec)):
            loc_i_j = z3.Int("L_{i}_{j}")
            loc_constraints.append(z3.And(loc_i_j >= 0, loc_i_j < num_args + num_comp))
            arg_constraints = []
            for arg_loc in range(num_args):
                arg_constraints.append(pi[i] + num_args == locations[arg_loc])

            
            o_constraints = [z3.And(pi[i] == locations[num_args+j], j < pi[i]+num_args) for j in range(num_comp)]
            constraints.append(z3.Or(*(arg_constraints + o_constraints)))
        ########## thing from whiteboard

        # I_pi_i = A1 | ... | I_pi_i = Am | ( |_{k=0,...n-1} (I_pi_i = Ok and k < pi[i]))

        # LLeq(I_pi_i, A1) or ... or LLeq(I_pi_i, Am) or (I_pi_i = O0 and 0 < pi[i]) or (I_pi_i = O1 and 1 < pi[i]) or (I_pi_i = O2 and 2 < pi[i]) or ... or (I_pi_i = On and n-1 < pi[i])


    all_constraints = pi_range + [ordering] + constraints
    return all_constraints

def LLeq(l1, l2):
    constraint_lst = [l1[i][j] == l2[i][j] for j in range(len(l1[0])) for i in range(len(l1))]
    return constraint_lst

def all(ll):
    bo = True
    for l in ll:
        if type(l) == list:
            for b in l:
                bo = bo and b
        else:
            bo = bo and l
    return bo

def find_dist_constraint(examples, program_candidate, components):
    return None

def main():
    # return ogis(somefunc)
    return test_synthesize()


def test_synthesize():
    oracle = lambda x: x + x
    ogis(oracle)

    return

    ex_set = []
    example = np.array([1,2,3,4]).reshape((2,2))
    example = np.array([[1]]) 
    ex_set.append((example, oracle(example)))

    input_shape = example.shape

    components = Components({'transpose': 0, 'eye_like': 0, 'ones_like': 0, 'multiply': 0, 'add': 1, 'matmul': 0}, input_shape).get_list()

    program = synthesize(ex_set, components)
    print(program)

if __name__ == '__main__':
    main()
