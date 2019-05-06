from z3 import *

class Components:
    component_num = -1
    components_list = []

    def __init__(self, counter, input_shape):
        for component, num in counter.items():
            for _ in range(num):
                self.components_list.append((component, getattr(Components, component)(self, input_shape)))
    
    def get_list(self):
        return [v for k,v in self.components_list]

    def get_names_from_indices(self, indices):
        return [self.components_list[i][0] for i in indices]

    def get_name(self):
        self.component_num += 1
        return f"T_{self.component_num}"

    def eye_like(self, shape):
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])),) # row major
        O = tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0]))
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                if row == col:
                    phi.append(And(O[row][col] == 1))
                else:
                    phi.append(And(O[row][col] == 0))
        return (I, O, And(*phi))
    
    def ones_like(self, shape):
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])),)
        O = tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0]))
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(And(O[row][col] == 1))
        return (I, O, And(*phi))

    def transpose(self, shape):
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])),)
        O = tuple(tuple(Int(self.get_name()) for i in range(shape[0])) for j in range(shape[1]))
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(And(O[col][row] == I[0][row][col]))
        return (I, O, And(*phi))

    def multiply(self, shape):
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])),
             tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])))
        O = tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0]))
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(And(O[row][col] == I[0][row][col] * I[1][row][col]))
        return (I, O, And(*phi))

    def add(self, shape):
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])),
             tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0])))
        O = tuple(tuple(Int(self.get_name()) for j in range(shape[1])) for i in range(shape[0]))
        phi = []
        for row in range(shape[0]):
            for col in range(shape[1]):
                phi.append(And(O[row][col] == I[0][row][col] + I[1][row][col]))
        return (I, O, And(*phi))

    def matmul(self, shape1):
        #assert shape1[1] == shape2[0]
        I = (tuple(tuple(Int(self.get_name()) for j in range(shape1[1])) for i in range(shape1[0])),
             tuple(tuple(Int(self.get_name()) for j in range(shape1[1])) for i in range(shape1[0])))
        O = tuple(tuple(Int(self.get_name()) for j in range(shape1[1])) for i in range(shape1[0]))
        phi = []
        for row in range(shape1[0]): # match output dimensions
            for col in range(shape1[1]):
                n = 0 
                for inner in range(shape1[1]):
                    n += I[0][row][inner] * I[1][inner][col]
                phi.append(And(O[row][col] == n))
        return (I, O, And(*phi))



