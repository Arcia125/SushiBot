class Customer(object):
    list = []
    def __init__(self, table, order):
        self.list.append(self)
        self.table = table
        self.order = order

    def is_waiting(self):
        pass

    def done_waiting(self):
        pass
