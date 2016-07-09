class Ingredient(object):
    list = []

    def __init__(self, name, default_amount, location, order_location, unavailable_color):
        self.list.append(self)
        self.name = name
        self.default_amount = default_amount
        self.location = location
        self.order_location = order_location
        self.unavailable_color = unavailable_color
        self.amount = default_amount

    @property
    def amount(self):
        return self.amount

    @amount.setter
    def amount(self, amount):
        self.amount = amount

    def reset_amount(self):
        self.amount = self.default_amount
