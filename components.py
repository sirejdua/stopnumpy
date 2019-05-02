import z3

class Components:
    component_num = 0
    def __init__(self, fn_lst):
        return

    def validate_program(self, components):
    # what other functionos should a components class be?
        return

    def transpose(shape):
        return

    def multiply(shape1, shape2):
        return

    def add(shape):
        return

    def eye_like(shape):
        return
    
    def ones_like(shape):
        return [z3.Int("o_%s_%s_%s".format(component_num, i, j))  for i in range(shape[0]) for j in range(shape[1])]



