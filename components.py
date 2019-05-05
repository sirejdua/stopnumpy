import z3

class Components:
    component_num = 0
    components_list = []

    def __init__(self, counter, input_shape):
        for component, num in counter.items():
            for _ in range(num):
                self.components_list.append(getattr(Components, component)(self, input_shape))
    
    def get_list(self):
        return self.components_list

    def get_name(self):
        self.component_num += 1
        return f"T_{self.component_num}"

    def eye_like(self, shape):
        I = [[[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]] # row major
        O = [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                if row == col:
                    phi.append(z3.And(O[row][col] == z3.Int(1)))
                else:
                    phi.append(z3.And(O[row][col] == z3.Int(0)))
        return (I, O, phi)
    
    def ones_like(self, shape):
        I = [[[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == z3.Int(1)))
        return (I, O, phi)

    def transpose(self, shape):
        I = [[[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(self.get_name()) for i in range(shape[0])] for j in range(shape[1])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[col][row] == I[0][row][col]))
        return (I, O, phi)

    def multiply(self, shape):
        I = [[[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])],
             [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == I[0][row][col] * I[1][row][col]))
        return (I, O, phi)

    def add(self, shape):
        I = [[[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])],
             [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]]
        O = [[z3.Int(self.get_name()) for j in range(shape[1])] for i in range(shape[0])]
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(z3.And(O[row][col] == I[0][row][col] + I[1][row][col]))
        return (I, O, phi)

    def matmul(self, shape1):
        #assert shape1[1] == shape2[0]
        I = [[[z3.Int(self.get_name()) for j in range(shape1[1])] for i in range(shape1[0])],
             [[z3.Int(self.get_name()) for j in range(shape1[1])] for i in range(shape1[0])]]
        O = [[z3.Int(self.get_name()) for j in range(shape1[1])] for i in range(shape1[0])]
        phi = []
        for row in range(shape1[0]): # match output dimensions
            for col in range(shape1[1]):
                n = z3.Int(0)
                for inner in range(shape1[1]):
                    n += I[0][row][inner] * I[1][inner][col]
                phi.append(z3.And(O[row][col] == n))
        return (I, O, phi)



