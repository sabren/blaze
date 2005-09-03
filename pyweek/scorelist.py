"""
Rawr!

Should anything to do with display be in this code?
  (i.e. ScoreList.print(xoffset, yoffset, color) or something similar)
"""

import unittest


"""
A great score list!
"""
class ScoreList:
    def __init__(self, names=[], scores=[], maxScores=10):
        self.scores = scores
        self.names = names
        self.maxScores = maxScores

        #self.reorder()

    def getScores(self):
        # list = self.names
        #num = 0
        #for name in list:
        #    list.insert(num, self.scores[num])
        #    num = num / 2
            
        return zip(self.names, self.scores)

    def giveScore(self, score):
        """
        Add a score if it's good enough
        """
        name = score[0]
        score = score[1]
        num = 0
        while score < num:
            num = num + 1
        if not num:
            self.scores.reverse()
            self.names.reverse()
            self.scores.append(score)
            self.names.append(name)
            self.scores.reverse()
            self.names.reverse()                    
        else:
            self.scores.insert(num+1, score)
            self.names.insert(num+1, name)
        #no longer needed here
        # self.scores.append (score)
        # self.reorder()
        if len(self.scores) > self.maxScores:
            self.scores.pop ()

    def reorder(self):
        """
        Sort the scores in descending order
        """
        self.scores.sort()
        self.scores.reverse()


"""
Just to make sure everything works right...
"""
class ScoreListTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        scoreList = ScoreList (['AAA', 'BBB', 'CCC', 'DDD', 'EEE'], [1, 2, 3, 4, 5])
        
        scoreList.giveScore (['FFF', 6])
        scoreList.giveScore (['GGG', 7])
        scoreList.giveScore (['HHH', 8])
        print scoreList.getScores()

#        assert scoreList.scores == [6, 5, 5, 4, 4], "Le wtf, sir."

        
if __name__=="__main__":
    unittest.main()
