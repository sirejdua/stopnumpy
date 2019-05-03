import z3

class Components:
    component_num = 0
    def __init__(self, fn_lst):
        return

    def validate_program(self, components):
    # what other functionos should a components class be?
        return

    def eye_like(shape):
        I = [[[z3.Int(f'mult_i1_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(f'mult_o_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                if row == col:
                    phi.append(z3.And(O[row][col] == z3.Int(1)))
                else:
                    phi.append(z3.And(O[row][col] == z3.Int(0)))
        return (I, O, phi)
    
    def ones_like(shape):
        I = [[[z3.Int(f'mult_i1_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(f'mult_o_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == z3.Int(1)))
        return (I, O, phi)

    def transpose(shape):
        I = [[[z3.Int(f'tranpose_i_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]] # row major
        O = [[z3.Int(f'tranpose_o_{j}_{i}') for i in range(shape[0])] for j in range(shape[1])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[col][row] == I[0][row][col]))
        return (I, O, phi)

    def multiply(shape):
        I = [[[z3.Int(f'mult_i1_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])],
             [[z3.Int(f'mult_i2_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(f'mult_o_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == I[0][row][col] * I[1][row][col]))
        return (I, O, phi)

    def add(shape):
        I = [[[z3.Int(f'mult_i1_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])],
             [[z3.Int(f'mult_i2_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(f'mult_o_{i}_{j}') for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == I[0][row][col] + I[1][row][col]))
        return (I, O, phi)

    def matmul(shape1, shape2):
        assert shape1[1] == shape2[0]
        I = [[[z3.Int(f'matmul_i1_{i}_{j}') for j in range(shape1[1])] for i in range(shape1[0])],
             [[z3.Int(f'matmul_i2_{i}_{j}') for j in range(shape2[1])] for i in range(shape2[0])]]
        O = [[z3.Int(f'matmul_o_{i}_{j}') for j in range(shape2[1])] for i in range(shape1[0])]
        phi = []
        for row in range(shape1[0]): # match output dimensions
            for col in range(shape2[1]):
                n = z3.Int(0)
                for inner in range(shape1[1]):
                    n += I[0][row][inner] * I[1][inner][col]
                phi.append(z3.And(O[row][col] == n))
        return (I, O, phi)
