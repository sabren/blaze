"""health.py -- keep track of our hero's health.

Okay, we're going to need:

* calorie system
  - food
  - calories affect counters
  - change body type

Calories are just going to be integers that we sling around.

At the heart of everything will be calorie banks, which keep accounts.
However, all anybody else really needs to worry about is the
HelthModel and HealthModelConfig.

Here, let me show a usage example:
"""
import unittest
class ExampleTest(unittest.TestCase):
    def testHealthExample(self):
        """We need a working tutorial.

        And here it is!
        """
        # First, we need to set up our configuration.
        hc = HealthModelConfig()

        # We could go with the defaults, but here are the options:
        hc.setStartFat(5000) # How many fat calories to start with
        hc.setStartBlood(1000) # How many blood sugar calories to start
        hc.setBloodLimit(1000) # Max blood sugar before fat uptake
        hc.setExertionRatio(50) # Calories to burn per exertion level
        hc.setLowBloodLevel(100) # Min blood sugar before recovering from fat
        hc.setRecoveryRate(5) # Blood sugar recovery rate, in calories/step()

        # Okay, now we pass the configuration to our new health model:
        h = HealthModel(hc)

        # We can find out where our calorie levels are at:
        self.assertEqual(h.getBlood(), 1000)
        self.assertEqual(h.getFat(), 5000)

        # So, now we've got all these calories.  Let's exert ourselves.
        h.exert(1)
        self.assertEqual(h.getBlood(), 950)
        # Remember that ExertionRatio?  For each exertion level,
        # we burn 50 blood sugar calories.
        h.exert(5)
        self.assertEqual(h.getBlood(), 700)

        # Now, what happens if we work too hard
        # and run out of blood sugar?
        h.exert(15)
        # Whew! We just burned 750 calories!
        self.assertEqual(h.getBlood(), 0)
        # Where'd the other 50 calories come from?
        # Why, we burned off fat, of course.
        self.assertEqual(h.getFat(), 4950)

        # Now, look what happens when we step() and update the model:
        h.step()
        self.assertEqual(h.getBlood(), 5)
        self.assertEqual(h.getFat(), 4945)

"""
It's that simple.  Read on for the rest of the tests and code.
"""


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
        self.__calories = calories

    def getCalories(self):
        """How many calories do I have left?
        """
        return self.__calories

    def addCalories(self, calories):
        """Yum.  Calories.
        """
        self.__calories = self.__calories + calories

    def burnCalories(self, calories):
        """Getting more hungry...

        If we burn more calories than we have, then we throw a
        NotEnoughCalories exception and pass along the debt.
        """
        self.__calories = self.__calories - calories
        if self.__calories < 0:
            calories_short = abs(self.__calories)
            self.__calories = 0 
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
        """We need initial blood sugar calories
        """
        self.c.setStartBlood(1001)
        self.assertEqual(self.c.getStartBlood(), 1001)

    def testConfigBloodLimit(self):
        """We need a blood sugar limit after which we convert to fat.
        """
        self.c.setBloodLimit(1001)
        self.assertEqual(self.c.getBloodLimit(), 1001)

    def testConfigExertionRatio(self):
        """We need the number of calories to burn per exertion level.
        """
        self.c.setExertionRatio(51)
        self.assertEqual(self.c.getExertionRatio(), 51)

    def testConfigLowBloodLevel(self):
        """We need a low blood sugar level.
        """
        self.c.setLowBloodLevel(101)
        self.assertEqual(self.c.getLowBloodLevel(), 101)

    def testConfigRecoveryRate(self):
        """We need a rate to restore low blood sugar.
        """
        self.c.setRecoveryRate(6)
        self.assertEqual(self.c.getRecoveryRate(), 6)
            

class HealthModelConfig:
    """Configuration for our Health Model.

    We set up our configurations, then pass this to our health model
    when we initialize.

    Takes no parameters.  Either stick with the defaults and go, or
    set new ones.
    """
    def __init__(self):
        self.__startfat = 5000
        self.__startblood = 1000
        self.__bloodlimit = 1000
        self.__exratio = 50
        self.__lowbloodlevel = 100
        self.__bloodrecoveryrate = 5

    def setStartFat(self, calories):
        """Set our starting fat calories.
        """
        self.__startfat = calories

    def getStartFat(self):
        """Get our starting fat calories.
        """
        return self.__startfat

    def setStartBlood(self, calories):
        """Set our starting blood sugar calories.
        """
        self.__startblood = calories

    def getStartBlood(self):
        """Get our starting blood calories.
        """
        return self.__startblood

    def setBloodLimit(self, calories):
        """Set our blood sugar limit, before fat uptake kicks in.
        """
        self.__bloodlimit = calories

    def getBloodLimit(self):
        """Get our blood sugar limit, before fat uptake kicks in.
        """
        return self.__bloodlimit

    def setLowBloodLevel(self, calories):
        """Set our low blood sugar level.

        If blood sugar gets too low, we start drawing from fat reserves.
        """
        self.__lowbloodlevel = calories

    def getLowBloodLevel(self):
        """Set our low blood sugar level.

        If blood sugar gets too low, we start drawing from fat reserves.
        """
        return self.__lowbloodlevel

    def setExertionRatio(self, calories):
        """Set our exertion ration.

        That's the number of calories burned per exertion level.
        """
        self.__exratio = calories

    def getExertionRatio(self):
        """Get our exertion ration.

        That's the number of calories burned per exertion level.
        """
        return self.__exratio

    def setRecoveryRate(self, rate):
        """Set our low blood sugar uptake rate, in calories per step().
        """
        self.__bloodrecoveryrate = rate

    def getRecoveryRate(self):
        """Get our low blood sugar uptake rate, in calories per step().
        """
        return self.__bloodrecoveryrate

class FoodTest(unittest.TestCase):
    """We'll need food to eat to give us calories.
    """
    def setUp(self):
        self.f = Food(150, 10) # Sugar, fat

    def testFoodCalories(self):
        """Must... eat... food...
        """
        self.assertEqual(self.f.consumed(), (150,10))

class Food:
    """Food is for the eatin'.  Or sub-classing.

    Consume all flesh!
    """
    def __init__(self, sugar, fat):
        self.nutrition = (sugar, fat)

    def consumed(self):
        """You have been eaten by a large kiwi bird.

        Hope you invested in life insurance.  Have a nice day.
        """
        return self.nutrition
    

class HealthModelTest(unittest.TestCase):
    """This is what a HealthModel is going to do.
    """
    def setUp(self):
        """
        We're going to explicitly declare our defaults, in case the
        coded defaults change.  They're not really important.
        """
        self.c = HealthModelConfig()
        self.c.setStartFat(5000)
        self.c.setStartBlood(1000)
        self.c.setBloodLimit(1000)
        self.c.setExertionRatio(50)
        self.c.setLowBloodLevel(100)
        self.c.setRecoveryRate(5)
        self.h = HealthModel(self.c)
        self.f = Food(100, 100)


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

    def testStrenuousExertion(self):
        """Let's use more calories than our blood sugar has.

        The remainder should be burned from fat calories.
        """
        self.h.exert(21) # This will burn 1050 calories.
        self.assertEqual(self.h.getFat(), 4950)

    def testEat(self):
        """Chow down!  Can we?

        Of course, eating food raises your blood sugar.
        The fat goes straight to your hips.
        """
        # We don't want to worry about our blood sugar limit yet.
        self.h.exert(2) # This will burn 100 blood sugar calories.
        self.h.eat(self.f)
        self.assertEqual(self.h.getFat(), 5100)
        self.assertEqual(self.h.getBlood(), 1000)

    def testEatSweets(self):
        """Too much sugar should turn to fat.
        """
        self.h.eat(self.f)
        self.assertEqual(self.h.getBlood(), 1000)
        self.assertEqual(self.h.getFat(), 5200)

    def testLowBloodSugar(self):
        """Low blood sugar should recover from fat.
        """
        self.h.exert(20) # Burn 1000 calories.
        self.assertEqual(self.h.getBlood(), 0)
        self.h.step() # Update the model another step.
        self.assertEqual(self.h.getBlood(), 5)
        
class HealthModel:
    """With this health model, we'll keep track of our hero's health.

    A HealthModel needs a HealthModelConfig and a HealthModelHandler.
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
        """Exertion burns calories.

        Level is multiplied by ExertionRatio to get number of
        calories burned.
        """
        try:
            self.blood.burnCalories(level*self.config.getExertionRatio())
        except NotEnoughCalories, e:
            # If we're short on blood sugar, burn fat.
            self.fat.burnCalories(e.calories_short)

    def eat(self, food):
        """Eat food.  Keep your strength up.

              BURGER TIME!
              Oh boy!
              Aarw... howmf! Hmff, kmff. MMF! Delifiouf!

              http://www.livejournal.com/users/jamtorkberg/64366.html  :)
        """
        calories = food.consumed() # (sugar, fat)
        self.blood.addCalories(calories[0])
        self.fat.addCalories(calories[1])
        if self.getBlood() > self.config.getBloodLimit():
            calories2fat = self.getBlood() - self.config.getBloodLimit()
            self.blood.burnCalories(calories2fat)
            self.fat.addCalories(calories2fat)

    def step(self):
        """Update the model.

        Things this will do:
        * If blood sugar is low, recover from fat.
        """
        if self.getBlood() < self.config.getLowBloodLevel():
            self.fat.burnCalories(self.config.getRecoveryRate())
            self.blood.addCalories(self.config.getRecoveryRate())

class HealthModelHandlerTest(unittest.TestCase):
    """We'll need an event handler for health-related events.
    """
    def testEventHandler(self):
        """Is there an EventHandler in the house?
        
        Hello.  We're from the government, and we're here to handle
        your events.
        """
        self.c = HealthModelConfig()
        self.h = HealthModel(self.c)
        self.handler = HealthModelHandler(self.h)
        
"""
Looks like we're going to use EventNet for our event handling.
Seems simple enough.
-> http://lgt.berlios.de/#eventnet
"""
import eventnet.driver

class HealthModelHandler(eventnet.driver.Handler):
    """
    """
    def __init__(self, model):
        self.model = model

"""
Here's what's left:

* Handle fat->blood calorie transfer
* Set up an event handler.
  * Need to know what events we need to handle.
"""

if __name__ == "__main__":
    unittest.main()
