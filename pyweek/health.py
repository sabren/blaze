"""health.py -- keep track of our hero's health.

Okay, we're going to need:

* calorie system
  - food
  - calories affect counters
  - change body type

Calories are just going to be integers that we sling around.
"""

import unittest
class CalorieBankTest(unittest.TestCase):
    """We would like a Calorie Bank to keep track of deposits and
    withdrawals.

    It'll just be a simple calorie accountant, who will complain
    loudly if we burn too many.
    """
    def setUp(self):
        self.c = CalorieBank(100) # start off with initial 100 calories

    # calorie report
    def testReport(self):
        """We'll need a report of how many calories we have.
        """
        self.assertEqual(100, self.c.getCalories())

    # add calories
    def testAdd(self):
        """We need to be able to add calories.
        """
        self.c.addCalories(50)
        self.assertEqual(150, self.c.getCalories())

    # use calories
    def testBurn(self):
        """We need to be able to burn calories.
        """
        self.c.burnCalories(50)
        self.assertEqual(50, self.c.getCalories())

    def testDontUseTooMany(self):
        """We need to raise an exception if we burn too many.
        """
        self.assertRaises(NotEnoughCalories, self.c.burnCalories, 150)

    def testGetImbalance(self):
        """If we use too many calories, we need to know the debt.

        We're going to pass this as an argument to the exception.
        Whoever is burning the calories will have to deal with it.
        """
        try:
            self.c.burnCalories(150)
        except NotEnoughCalories, e:
            self.assertEqual(e.calories_short, 50)

class HealthError(Exception): pass
class NotEnoughCalories(HealthError):
    """CalorieBank throws this when you burn too many calories.

    The calories left to burn are stored in calories_short
    """
    def __init__(self, args=None):
        self.args = args
        self.calories_short = args

class CalorieBank:
    """Calories == Energy.  Eat lots, don't work too hard.
    """
    def __init__(self, calories):
        self.calories = calories

    def getCalories(self):
        """How many calories do I have left?
        """
        return self.calories

    def addCalories(self, calories):
        """Yum.  Calories.
        """
        self.calories = self.calories + calories

    def burnCalories(self, calories):
        """Getting more hungry...
        """
        self.calories = self.calories - calories
        if self.calories < 0:
            calories_short = abs(self.calories)
            self.calories = 0 # reset to zero
            raise NotEnoughCalories, calories_short

"""
The Health Model will store calories:
  - as blood sugar
    - blood sugar is our immediate energy source
    - when we have lots of blood sugar, it turns to fat
  - as fat
    - fat makes us bigger
    - when blood sugar gets low, fat converts to blood sugar

Exertion:
  - exertion will use calories.
  - the amount depends on the level of exertion.
  - we'll keep the exertion:calories ration configurable.  Default is 1:50
"""

class HealthModelConfigTest(unittest.TestCase):
    """This is how we'll configure our health model.
    """
    def setUp(self):
        self.c = HealthModelConfig()
        
    def testConfigStartFat(self):
        """Initial fat calories
        """
        self.c.setStartFat(5001)
        self.assertEqual(self.c.getStartFat(), 5001)

    def testConfigStartBlood(self):
        """Initial blood sugar calories
        """
        self.c.setStartBlood(1001)
        self.assertEqual(self.c.getStartBlood(), 1001)

    def testConfigBloodLimit(self):
        """Blood sugar limit before we start converting to fat.
        """
        self.c.setBloodLimit(1001)
        self.assertEqual(self.c.getBloodLimit(), 1001)

    def testConfigExertionRatio(self):
        """How many calories to burn per exertion level.
        """
        self.c.setExertionRatio(51)
        self.assertEqual(self.c.getExertionRatio(), 51)

class HealthModelConfig:
    """Configuration for our Health Model.

    We set up our configurations, then pass this to our health model
    when we initialize.

    Takes no parameters.  Either stick with the defaults and go, or
    set new ones.
    """
    def __init__(self):
        self.startfat = 5000
        self.startblood = 1000
        self.bloodlimit = 1000
        self.exratio = 50

    def setStartFat(self, calories):
        """Set our starting fat calories.
        """
        self.startfat = calories

    def getStartFat(self):
        """Get our starting fat calories.
        """
        return self.startfat

    def setStartBlood(self, calories):
        """Set our starting blood sugar calories.
        """
        self.startblood = calories

    def getStartBlood(self):
        """Get our starting blood calories.
        """
        return self.startblood

    def setBloodLimit(self, calories):
        """Set our blood sugar limit, before fat uptake kicks in.
        """
        self.bloodlimit = calories

    def getBloodLimit(self):
        """Get our blood sugar limit, before fat uptake kicks in.
        """
        return self.bloodlimit

    def setExertionRatio(self, calories):
        """Set our exertion ration.

        That's the number of calories burned per exertion level.
        """
        self.exratio = calories

    def getExertionRatio(self):
        """Get our exertion ration.

        That's the number of calories burned per exertion level.
        """
        return self.exratio
    

class FoodTest(unittest.TestCase):
    """We'll need food to eat to give us calories.
    """
    def setUp(self):
        self.f = Food(150)
        
    

class HealthModelTest(unittest.TestCase):
    """This is what a HealthModel is going to do.
    """
    def setUp(self):
        self.c = HealthModelConfig()
        self.c.setStartFat(5000)
        self.c.setStartBlood(1000)
        self.c.setBloodLimit(1000)
        self.c.setExertionRatio(50)
        self.h = HealthModel(self.c)

    def testConfig(self):
        """We'll need to retrieve our configuration.
        """
        self.assertEqual(self.h.getConfig(), self.c)

    def testFatReport(self):
        """We'll need a fat calorie report.
        """
        self.assertEqual(self.h.getFat(), 5000)

    def testBloodReport(self):
        """We'll need a blood sugar calorie report.
        """
        self.assertEqual(self.h.getBlood(), 1000)


    def testExertion(self):
        """We should be able to exert ourselves.

        This should lower our available blood sugar calories.
        """
        self.h.exert(1)
        self.assertEqual(self.h.getBlood(), 950)
        

class HealthModel:
    """With this health model, we'll keep track of our hero's health.
    """
    def __init__(self, config):
        self.config = config
        self.fat = CalorieBank(self.config.getStartFat())
        self.blood = CalorieBank(self.config.getStartBlood())

    def getConfig(self):
        return self.config
        
    def getFat(self):
        return self.fat.getCalories()

    def getBlood(self):
        return self.blood.getCalories()

    def exert(self, level):
        self.blood.burnCalories(level*self.config.getExertionRatio())

"""
Here's what's left:

* Finish the exertion code
* Handle fat->blood calorie transfer
* Handle food and eating
* Make the Health Model update itself on each .step()
"""

if __name__ == "__main__":
    unittest.main()
