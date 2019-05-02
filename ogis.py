import z3
import numpy as np

# OGIS

def main():
	oracle = some_func
	ex_set = {}

	components = []
	populate_components()

	example = np.ones((2,2))


	while example is not None:
		ex_set[example] = oracle(example)

		program_candidate = synthesize(ex_set, components)

		if program_candidate is None:
			#change components?
			pass


		example = find_dist_constraint(ex_set, program_candidate, components)


if __name__ == '__main__':
	main()