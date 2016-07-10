import logging

logging.basicConfig(format='%(asctime)s %(message)s', filemode='w', filename='ingredient_debug.log',
                    level=logging.DEBUG)

class Ingredient(object):
    list = []

    def __init__(self, name, default_amount, location, order_location, unavailable_color):
        """

        :param name: name of ingredient
        :type name: str
        :param default_amount: starting amount of ingredient
        :type default_amount: int
        :param location: coordinates of the use button for ingredient
        :type location: tuple
        :param order_location: coordinates of the order button for ingredient
        :type order_location: tuple
        :param unavailable_color: 3 value tuple that describes unavailable color of ingredient
        :type unavailable_color: tuple
        """
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
        logging.debug('Reset amount of {}'.format(self.name))
