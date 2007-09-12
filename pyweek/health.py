"""
health.py -- keep track of our hero's health.

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
import unittest, room

class ExampleTest(unittest.TestCase):
    def setUp(self):
        """
        Don't worry about this.

        This will just keep eventnet from complaining about our
        unhandled events in the test.
        """
        pass
        
    def testHealthExample(self):
        """
        We need a working tutorial.

        And here it is!
        """
        # First, we need to set up our configuration.
        hc = HealthModelConfig()

        # We could go with the defaults, but here are the options:
        hc.startfat = 5000 # How many fat calories to start with
        hc.startblood = 1000 # How many blood sugar calories to start
        hc.bloodlimit = 1000 # Max blood sugar before fat uptake
        hc.exertionratio = 50 # Calories to burn per exertion level
        hc.lowbloodlevel = 100 # Min blood sugar before recovering from fat
        hc.bloodrecoveryrate = 5 # Blood sugar recovery rate, in calories/step()
        hc.baseinsulinrate = 2 # Insulin lowers blood sugar, in calories/step()
        hc.insulinratio = 10 # Insulin penalty ratio for high blood sugar.
        hc.suppressinsulin = False # If we suppress insulin, new rules take effect.
        hc.insulin2fatratio = .5 # How many of the calories lost to insulin go to fat?

        # Okay, now we pass the configuration to our new health model:
        h = HealthModel(hc)

        # HealthModel is its own event handler.  We need to start it up.
        h.capture()

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
        h.config.suppressinsulin = True # We'll deal with this later.
        h.step()
        self.assertEqual(h.getBlood(), 5)
        self.assertEqual(h.getFat(), 4945)

        # Sugar recovery is slow, so let's eat something.
        rm = room.Room()
        cake = Food(320, 10, rm, (10,10)) # 320 calories from sugar, 10 from fat
        h.eat(cake)
        self.assertEqual(h.getBlood(), 325)
        self.assertEqual(h.getFat(), 4955)

        # Much better.  But we're still hungry.
        powerbar = Food(700, 0, rm, (10,10))
        # MMmmm... carbs...
        h.eat(powerbar)
        self.assertEqual(h.getBlood(), 1000)
        # Wow.  Sugar rush.  But where are the other 25 calories?
        self.assertEqual(h.getFat(), 4980)
        # Ah.  When our blood sugar gets too high, it turns to fat.
        # Yep.  So realistic.

        # Okay, all that was with the insulin response suppressed.
        h.config.suppressinsulin = False # New rules!

        # Take a step...
        h.step()
        self.assertEqual(h.getBlood(), 998)
        # Did you catch that?
        # Insulin lowers your blood sugar at a slow rate.
        # Think of it as a cost-of-living tax.

        # But where do the calories go?
        self.assertEqual(h.getFat(), 4981)
        # Straight to the hips of course.
        # But only one of the two calories went over.
        # Insulin isn't very efficient at storing fat.
        # The rate is controlled by h.config.insulin2fatratio
        # In this case, it's 0.5 fat for every sugar

        # Hey kid, would you like some candy?
        candy = Food(102, 0, rm, (50,50))
        h.eat(candy)
        self.assertEqual(h.getBlood(), 1100)
        # Looks like we've got high blood sugar.
        h.step()
        self.assertEqual(h.getBlood(), 98)
        # Whoah! Sugar crash!
        # That's controlled by the h.config.insulinratio
        # In this case, it's 10 lost for every 1 above the limit
        # And 2 for the normal insulin rate.
        self.assertEqual(h.getFat(), 5482)
        # And half of that goes to fat.
        # Bleh.  I feel sick.  No more candy.
        

        # In summary:
        hc = HealthModelConfig()         ## set up default model config
        h = HealthModel(hc)              ## initialize a new model
        h.exert(level=5)                 ## exertion burns calories.
        food = Food(sugar=100, fat=100, room=rm, position=(50,50))  ## food can have different nutritional values
        h.eat(food)                      ## eating increases blood sugar and body fat
        h.step()                         ## updates the model, handles blood sugar and insulin

"""
It's that simple.  Read on for the rest of the tests and code.
"""


class CalorieBankTest(unittest.TestCase):
    """
    We would like a Calorie Bank to keep track of deposits and
    withdrawals.

    It'll just be a simple calorie accountant, who will complain
    loudly if we burn too many.
    """
    def setUp(self):
        self.c = CalorieBank(100) # start off with initial 100 calories

    # calorie report
    def testReport(self):
        """
        We'll need a report of how many calories we have.
        """
        self.assertEqual(100, self.c.getCalories())

    # add calories
    def testAdd(self):
        """
        We need to be able to add calories.
        """
        self.c.addCalories(50)
        self.assertEqual(150, self.c.getCalories())

    # use calories
    def testBurn(self):
        """
        We need to be able to burn calories.
        """
        self.c.burnCalories(50)
        self.assertEqual(50, self.c.getCalories())


    def testDontUseTooMany(self):
        """
        We need to raise an exception if we burn too many.
        """
        self.assertRaises(NotEnoughCalories, self.c.burnCalories, 150)

    def testGetImbalance(self):
        """
        If we use too many calories, we need to know the debt.

        We're going to pass this as an argument to the exception.
        Whoever is burning the calories will have to deal with it.
        """
        try:
            self.c.burnCalories(150)
        except NotEnoughCalories, e:
            self.assertEqual(e.calories_short, 50)

class HealthError(Exception): pass
class NotEnoughCalories(HealthError):
    """
    CalorieBank throws this when you burn too many calories.

    The calories left to burn are stored in calories_short
    """
    def __init__(self, args=None):
        try:
            self.args = args
        except:
            self.args = (args,)
        self.calories_short = args

class CalorieBank:
    """
    Calories == Energy.  Eat lots, don't work too hard.

    This is just a simple class that gets used by the HealthModel.
    """
    def __init__(self, calories):
        self.__calories = calories

    def getCalories(self):
        """
        How many calories do I have left?
        """
        return self.__calories

    def addCalories(self, calories):
        """
        Yum.  Calories.
        """
        self.__calories = self.__calories + calories

    def burnCalories(self, calories):
        """
        Getting more hungry...

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
    """
    This is how we'll configure our health model.
    """
    def setUp(self):
        self.c = HealthModelConfig()
        
    def testConfigStartFat(self):
        """
        Initial fat calories
        """
        self.assertEqual(self.c.startfat, 5000)

    def testConfigStartBlood(self):
        """
        We need initial blood sugar calories
        """
        self.assertEqual(self.c.startblood, 1000)

    def testConfigBloodLimit(self):
        """
        We need a blood sugar limit after which we convert to fat.
        """
        self.c.bloodlimit = 1000
        self.assertEqual(self.c.bloodlimit, 1000)

    def testConfigExertionRatio(self):
        """
        We need the number of calories to burn per exertion level.
        """
        self.c.exertionratio = 50
        self.assertEqual(self.c.exertionratio, 50)

    def testConfigLowBloodLevel(self):
        """
        We need a low blood sugar level.
        """
        self.c.lowbloodlevel = 100
        self.assertEqual(self.c.lowbloodlevel, 100)

    def testConfigRecoveryRate(self):
        """
        We need a rate to restore low blood sugar.
        """
        self.c.bloodrecoveryrate = 5
        self.assertEqual(self.c.bloodrecoveryrate, 5)

    def testConfigBaseInsulinRate(self):
        """
        We need a base rate at which to burn blood sugar.
        """
        self.c.baseinsulinrate = 2
        self.assertEqual(self.c.baseinsulinrate, 2)

    def testConfigInsulinRatio(self):
        """
        We need a ratio to figure the high blood sugar penalty.

        For every calorie above the high blood sugar limit, insulin
        will kill this many calories.
        """
        self.assertEqual(self.c.insulinratio, 10)

    def testConfigInsulin2FatRatio(self):
        """
        We need a ratio of the calories converted by insulin to fat.

        For every blood sugar calorie converted by insulin, this many
        go to fat.  Ought to be a float between 0 and 1
        """
        self.assertEqual(self.c.insulin2fatratio, 0.5)

class HealthModelConfig:
    """
    Configuration for our Health Model.

    We set up our configurations, then pass this to our health model
    when we initialize.

    Takes no parameters.  Either stick with the defaults and go, or
    set new ones.

    Variables to play with:
        startfat -- How many fat calories to start with
        startblood -- How many blood sugar calories to start
        bloodlimit -- Max blood sugar before fat uptake
        exertionratio -- Calories to burn per exertion level
        lowbloodlevel -- Min blood sugar before recovering from fat
        recoveryrate -- Blood sugar recovery rate, in calories/step()
        baseinsulinrate -- Insulin lowers blood sugar, in calories/step()
        insulinratio -- Insulin penalty ratio for high blood sugar.
        suppressinsulin -- suppresses the insulin response (mainly for testing)
        fatmass -- mass/fat calorie
        fatdensity -- area/fat calorie 
    """
    def __init__(self):
        # Set our starting fat calories.
        self.startfat = 5000
        # Set our starting blood sugar calories.
        self.startblood = 1000
        # Set our blood sugar limit, before fat uptake kicks in.
        self.bloodlimit = 1000
        # Set our exertion ration.
        self.exertionratio = 20
        # Set our low blood sugar level.
        self.lowbloodlevel = 100
        # Set our low blood sugar uptake rate, in calories/step().
        self.bloodrecoveryrate = 5
        # Set the base rate at which to burn blood sugar, in calories/step()
        self.baseinsulinrate = 2
        # Set the penalty ratio for high blood sugar.
        self.insulinratio = 10
        # Should we suppress the insulin response?
        self.suppressinsulin = False
        # Set the insulin2fat conversion ratio
        self.insulin2fatratio = 0.5

        #@TODO: these units are whatever ode uses. document!!
        # Set the amount of mass/fat calorie
        self.fatmass = 0.0001
        # Set the space taken up by a fat calorie
        self.fatspace = 1

class FoodTest(unittest.TestCase):
    """
    We'll need food to eat to give us calories.
    """
    def setUp(self):
        rm = room.Room()
        self.f = Food(150, 10, rm, (50,50)) # Sugar, fat

    def testFoodPhysics(self):
        """
        Food is a physical object, yes?
        """
        # this used to be an isinstance() test
        # but we don't really care about that,
        # only that it's something like an ode.GeomXXX
        assert self.f.geom.getPosition()

    def testFoodCalories(self):
        """
        Must... eat... food...
        """
        self.assertEqual(self.f.consumed(), (150,10))

import ode, constants
from constants import HERO
from constants import CODE # Michal's UgLy hack. :)
class Food:
    """
    Food is for the eatin'.  Or sub-classing.

    Consume all flesh!
    """
    def __init__(self, sugar, fat, room, position):
        self.nutrition = (sugar, fat)
        # @TODO: food should BE a geom, not own one. :(
        self.radius = HERO.RADIUS
        self.room = room    
        self.geom = self.room.addBlock(position,
                                       2*self.radius, 2*self.radius)
        self.geom.code = CODE.FOOD

    def consumed(self):
        """
        You have been eaten by a large kiwi bird.

        Hope you invested in life insurance.  Have a nice day.

        Oh, and the kiwi gets a tuple of nutrition (sugar, fat) for
        his trouble.
        """
        calories = self.nutrition
        self.nutrition = (0,0)
        return calories
    

class HealthModelTest(unittest.TestCase):
    """
    This is what a HealthModel is going to do.
    """
    def setUp(self):
        """
        We're going to explicitly declare our defaults, in case the
        coded defaults change.  They're not really important.
        """
        self.c = HealthModelConfig()
        self.c.startfat = 5000
        self.c.startblood = 1000
        self.c.bloodlimit = 1000
        self.c.exertionratio = 50
        self.c.lowbloodlevel = 100
        self.c.bloodrecoveryrate = 5
        self.c.baseinsulinrate = 2
        self.c.insulinratio = 10
        self.c.insulin2fatratio = 0.5
        self.h = HealthModel(self.c)
        self.h.capture()
        rm = room.Room()
        self.f = Food(100, 100, rm, (200,200))

    def testReports(self):
        """
        We'll need a fat calorie report.
        """
        self.assertEqual(self.h.getBlood(), 1000)
        self.assertEqual(self.h.getFat(), 5000)

    def testExertion(self):
        """
        We should be able to exert ourselves.

        This should lower our available blood sugar calories.
        """
        self.assertEqual(1000, self.h.getBlood())
        self.assertEqual(50, self.h.config.exertionratio)
        self.h.exert(1)
        self.assertEqual(950, self.h.getBlood())

    def testStrenuousExertion(self):
        """
        Let's use more calories than our blood sugar has.

        The remainder should be burned from fat calories.
        """
        self.h.exert(21) # This will burn 1050 calories.
        self.assertEqual(self.h.getFat(), 4950)

    def testEat(self):
        """
        Chow down!  Can we?

        Of course, eating food raises your blood sugar.
        The fat goes straight to your hips.
        """
        # We don't want to worry about our blood sugar limit yet.
        self.h.exert(2) # This will burn 100 blood sugar calories.
        self.h.eat(self.f)
        self.assertEqual(self.h.getFat(), 5100)
        self.assertEqual(self.h.getBlood(), 1000)

    def testInsulin(self):
        """
        Blood sugar should burn at a normal rate.
        """
        self.h.step()
        self.assertEqual(self.h.getBlood(), 998)

    def testEatSweets(self):
        """
        Too much sugar should trigger an insulin response.
        """
        self.h.eat(self.f)
        self.h.step()
        self.assertEqual(self.h.getBlood(), 98 ) # Insulin kills 2+10*100 calories

    def testSugarCrashEvent(self):
        """
        Losing too much sugar all at once should trigger a SUGAR_CRASH
        """
        self.h.eat(self.f)
        self.h.step()
        

    def testEatSweetsGetFat(self):
        """
        An insulin response converts some sugar to fat.
        """
        self.h.eat(self.f)
        self.h.step()
        self.assertEqual(self.h.getFat(), 5601) # Insulin produces (2+10*100)*0.5 calories of fat

    def testLowBloodSugar(self):
        """
        Low blood sugar should recover from fat.
        """
        self.h.exert(20) # Burn 1000 calories.
        self.assertEqual(self.h.getBlood(), 0)
        self.h.config.suppressinsulin = True # suppress insulin response
        self.h.step() # Update the model another step.
        self.assertEqual(self.h.getBlood(), 5)

# We'll need the event driver:
# http://lgt.berlios.de/#eventnet
import eventnet.driver

# We're going to need events to throw around.
from events import HEALTH


class HealthModel(eventnet.driver.Handler):
    """
    With this health model, we'll keep track of our hero's health.

    A HealthModel needs a HealthModelConfig and a HealthModelHandler.
    """
    def __init__(self, config):
        super(HealthModel, self).__init__()
        self.config = config
        self.fat = CalorieBank(self.config.startfat)
        self.blood = CalorieBank(self.config.startblood)

    def getFat(self):
        return self.fat.getCalories()

    def getBlood(self):
        return self.blood.getCalories()

    def exert(self, level):
        """
        Exertion burns calories.

        Level is multiplied by ExertionRatio to get number of
        calories burned.
        """
        try:
            self.blood.burnCalories(level*self.config.exertionratio)
        except NotEnoughCalories, e:
            # If we're short on blood sugar, burn fat.
            try:
                self.fat.burnCalories(e.calories_short)
            except NotEnoughCalories, e:
                eventnet.driver.post(EVENTS.HEALTH.STARVE)
            self.postFatChanged()
        self.postBloodChanged()

    def eat(self, food):
        """
        Eat food.  Keep your strength up.

              BURGER TIME!
              Oh boy!
              Aarw... howmf! Hmff, kmff. MMF! Delifiouf!

              http://www.livejournal.com/users/jamtorkberg/64366.html  :)
        """
        calories = food.consumed() # (sugar, fat)
        self.blood.addCalories(calories[0])
        self.fat.addCalories(calories[1])
        """
        We used to convert extra blood sugar calories to fat here.
        Now, however, step() will initiate an insulin response.

        However, we'll still do that if we have the insulin response
        suppressed:
        """
        if self.config.suppressinsulin == True:
            if self.getBlood() > self.config.bloodlimit:
                calories2fat = self.getBlood() - self.config.bloodlimit
                self.blood.burnCalories(calories2fat)
                self.fat.addCalories(calories2fat)
        self.postFatChanged()
        self.postBloodChanged()
        

    def step(self):
        """
        Update the model.

        Things this will do:
        * If blood sugar is low, recover from fat.
        * Burn blood sugar at normal insulin rate
        * If blood sugar is high, trigger an increased insulin response.
        """
        if self.getBlood() < self.config.lowbloodlevel:
            self.fat.burnCalories(self.config.bloodrecoveryrate)
            self.blood.addCalories(self.config.bloodrecoveryrate)
        if not self.config.suppressinsulin:
            insulinpenalty = 0
            if self.getBlood() > self.config.bloodlimit:
                eventnet.driver.post(HEALTH.HIGH_BLOOD)
                insulinpenalty = (self.getBlood() - self.config.bloodlimit) * self.config.insulinratio
            insulin = self.config.baseinsulinrate + insulinpenalty
            self.blood.burnCalories(insulin)
            if insulin > self.config.bloodlimit/2:
                # Looks like a sugar crash.
                eventnet.driver.post(HEALTH.SUGAR_CRASH)
            insulin2fat = int(insulin*self.config.insulin2fatratio)
            self.fat.addCalories(insulin2fat)
        self.postFatChanged()
        self.postBloodChanged()

    def postBloodChanged(self):
        newblood = self.getBlood()
        limit = 4*self.config.bloodlimit
        eventnet.driver.post(HEALTH.BLOOD_CHANGED, blood=newblood, ceiling=limit)

    def postFatChanged(self):
        newfat = self.getFat()
        limit = 4*self.config.startfat
        eventnet.driver.post(HEALTH.FAT_CHANGED, fat=newfat, ceiling=limit)
                         



        
                
"""
Here's what's left:

* Set up an event handler.
* Need to know what events we need to handle.
"""
                                                                          

if __name__ == "__main__":
    unittest.main()
