import logging
import win32api

import time
import win32con
from PIL import ImageGrab
from PIL import ImageOps
from numpy import *

import coordinates
import ingredients

logging.basicConfig(format='%(asctime)s %(message)s', filemode='w', filename='bot_debug.log', level=logging.DEBUG)

table_x = 26
table_y = 61

rice_u = (127, 127, 127)
nori_u = (33, 30, 11)
roe_u = (127, 61, 0)
shrimp_u = (127, 71, 47)
unagi_u = (94, 49, 8)
salmon_u = (127, 71, 47)

shrimp = ingredients.Ingredient('shrimp', 10, coordinates.shrimp, coordinates.phone_shrimp, shrimp_u)
rice = ingredients.Ingredient('rice', 10, coordinates.rice, coordinates.phone_rice, rice_u)
nori = ingredients.Ingredient('nori', 10, coordinates.nori, coordinates.phone_nori, nori_u)
roe = ingredients.Ingredient('roe', 10, coordinates.roe, coordinates.phone_roe, roe_u)
salmon = ingredients.Ingredient('salmon', 10, coordinates.salmon, coordinates.phone_salmon, salmon_u)
unagi = ingredients.Ingredient('unagi', 10, coordinates.unagi, coordinates.phone_unagi, unagi_u)

recipes = {'onigiri': {'rice': 2,
                       'nori': 1},
           'caliroll': {'rice': 1,
                        'nori': 1,
                        'roe': 1},
           'gunkan': {'rice': 1,
                      'nori': 1,
                      'roe': 2},
           'salmonroll': {'rice': 1,
                          'nori': 1,
                          'salmon': 2},
           'shrimpsushi': {'rice': 1,
                           'nori': 1,
                           'shrimp': 2},
           'unagiroll': {'rice': 1,
                         'nori': 1,
                         'unagi': 2},
           'dragonroll': {'rice': 2,
                          'nori': 1,
                          'roe': 1,
                          'unagi': 2},
           'combodish': {'rice': 2,
                         'nori': 1,
                         'salmon': 1,
                         'shrimp': 1,
                         'unagi': 1,
                         'roe': 1}
           }

class Bot(object):
    def __init__(self):
        self.x_pad = 464
        self.y_pad = 237
        self.tables = [0, 0, 0, 0, 0, 0]

    def mouse_pos(self, cords):
        win32api.SetCursorPos((self.x_pad + cords[0], self.y_pad + cords[1]))

    def click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def click_on(self, cords):
        self.mouse_pos(cords)
        self.click()
        time.sleep(.1)
        logging.debug('Clicked on {}'.format(cords))

    def get_current_mouse_pos(self):
        x, y = win32api.GetCursorPos()
        x -= self.x_pad
        y -= self.y_pad
        logging.debug('x = {} y = {}'.format(x, y))
        return x, y

    def draw_box(self):
        pass

    def make_box(self, left, top, right, bottom):
        box = (left + self.x_pad + 1, top + self.y_pad + 1, right + self.x_pad + 1, bottom + self.y_pad + 1)
        return box

    def screen_grab(self):
        x_pad2 = 641
        y_pad2 = 481
        box = self.make_box(0, 0, x_pad2, y_pad2)
        im = ImageGrab.grab(box)
        # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
        return im

    def grab_area(self, box):
        im = ImageGrab.grab(box)
        return im

    def get_grayscale_pixel_sum(self, image):
        """
        :param image: PIL image
        :type image: object
        :return: sum of pixels
        :rtype: int
        """
        gray_image = ImageOps.grayscale(image)
        image_array = array(gray_image.getcolors())
        pixel_sum = image_array.sum()
        return pixel_sum

    def start_game(self):
        self.click_on(coordinates.menu1)
        self.click_on(coordinates.menu2)
        self.click_on(coordinates.menu3)
        self.click_on(coordinates.menu4)
        logging.info('Game started!')

    def play_game(self):
        pass

    def get_tasks(self):
        pass

    def get_table_box(self, table_number):
        """
        Returns a table box for a given table number
        :type table_number: int
        :rtype: tuple
        """
        next_table = 101
        table_pad = next_table * table_number
        table_width = 61
        table_height = 14
        left = coordinates.table[0] + table_pad
        top = coordinates.table[1]
        right = left + table_width
        bottom = top + table_height
        box = self.make_box(left, top, right, bottom)
        return box

    def look_at_table(self, table_number):
        """
        Gets image of a table at given number
        :type table_number: int
        :rtype: object
        """
        table_image = self.grab_area(self.get_table_box(table_number))
        return table_image

    def look_at_all_tables(self):
        """
        :return: list of PIL images
        :rtype: list
        """
        tables = 6
        images = []
        for table in range(tables):
            table_image = self.look_at_table(table)
            images.append(table_image)
        return images

    def table_is_empty(self, table_number):
        """
        :param table_number: table number
        :type table_number: int
        :return: True if table is empty
        :rtype: bool
        """
        # empty seat pixel sums of tables 1-6
        empty_tables = [6434, 5832, 10536, 10228, 6290, 8689]
        table_image = self.look_at_table(table_number - 1)
        pixel_sum = self.get_grayscale_pixel_sum(table_image)
        return pixel_sum == empty_tables[table_number - 1]

    def is_new_customer(self, table_state, table_number):
        """
        Returns true if there is a new customer at this table
        :type table_state: bool
        :type table_number: int
        :return:
        :rtype:
        """
        return (table_state == False) and (self.tables[table_number - 1] == 0)

    def look_for_new_customers(self):
        for table_number_i in range(6):
            table_state = self.table_is_empty(table_number_i + 1)
            new = self.is_new_customer(table_state, table_number_i + 1)
            if new:
                self.tables[table_number_i] = 1

    def clear_tables(self):
        plates = [(92, 211), (197, 211), (295, 211), (397, 211), (495, 211), (595, 211), (603, 211), (617, 211)]
        for plate in plates:
            self.click_on(plate)
        logging.info('Clearing tables')
        time.sleep(.5)

    def make_food(self, food):
        logging.info('Making {}'.format(food))
        recipe = recipes[food]
        for ingredient, amount in recipe.items():
            logging.info('Recipe for {} is {} {}'.format(food, amount, ingredient))
            for i in amount:
                self.click_on(eval(ingredient).location)

    def take_order(self, table):
        pass

    def take_orders(self):
        pass

    def run_routines(self):
        pass

    def next_level(self):
        pass

    def fold_mat(self):
        self.click_on(coordinates.mat)

    def use_ingredient(self, ingredient):
        self.click_on(ingredient.location)
