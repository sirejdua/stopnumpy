class Oracle:
    def __init__(self):
        return

    def query(self, input):
        raise NotImplementedError
        return

    def get_pair(self, input):
        return self.query(self.random_input())

    def random_input(self):
        raise NotImplementedError
        return

