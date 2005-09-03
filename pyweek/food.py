from health import Food

MULTI = 1.0 # A multiplier for if we need to quickly increase how many
            # calories foodstuffs are worth.
MENU = { # Of the form "foodname":(sugar, fat)
    "waffle":(500,0),
    "burger":(60, 500)
    }

import unittest
class TestFoodFactory(unittest.TestCase):
    def setUp(self):
        self.ff = FoodFactory()

    def testOrder(self):
        food = self.ff.order("waffle")
        assert isinstance(food, Food)
        self.assertEqual(food.nutrition[0], 500*MULTI)
        self.assertEqual(food.nutrition[1], 0*MULTI)
        
class FoodFactory:
    def __init__(self):
        self.menu = MENU

    def order(self, type):
        sugar, fat = self.menu[type]
        return Food(int(sugar*MULTI), int(fat*MULTI)) 


if __name__ == "__main__":
    unittest.main()
    
        


    
