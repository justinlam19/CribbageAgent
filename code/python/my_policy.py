from policy import CribbagePolicy, CompositePolicy
from my_throw_policy import MyThrower
from my_peg_policy import MyPegger

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._policy = CompositePolicy(game, MyThrower(game), MyPegger(game))

        
    def keep(self, hand, scores, am_dealer):
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, turn, scores, am_dealer):
        return self._policy.peg(cards, history, turn, scores, am_dealer)                                    
