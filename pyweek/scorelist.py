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
    def __init__(self, scores=[], maxScores=10):
        self.scores = scores
        self.maxScores = maxScores

        self.reorder()

    def giveScore(self, score):
        """
        Add a score if it's good enough
        """
        if len(self.scores) < self.maxScores:
            self.scores.append (score)
            self.reorder()
        else:
            closest = None
            
            for s in self.scores:
                if closest == None or s-score < closest:
                    closest = s-score

            self.scores.pop (self.scores.index (closest+score))
            self.scores.append (score)
            self.reorder()

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
        scoreList = ScoreList ([1, 2, 3, 4, 5], 3)
        
        scoreList.giveScore (6)
        scoreList.giveScore (4)
        scoreList.giveScore (5)

        assert scoreList.scores == [6, 5, 5, 4, 4], "Le wtf, sir."

        
if __name__=="__main__":
    unittest.main()
