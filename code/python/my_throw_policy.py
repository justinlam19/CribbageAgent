from itertools import combinations
import pickle
import random
import scoring
from policy import ThrowPolicy


class MyThrower(ThrowPolicy):
    """ My cribbage pegging policy.
    """
    def __init__(self, game):
        """ Creates a greedy keep/throw policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)
        with open("dealer.pkl", "rb") as f:
            self.dealer_table = pickle.load(f)
        with open("nondealer.pkl", "rb") as f:
            self.nondealer_table = pickle.load(f)
    

    def table_get(self, i, j, am_dealer):
        if am_dealer:
            return self.dealer_table[i - 1][j - 1]
        else:
            return self.nondealer_table[i - 1][j - 1]


    def keep(self, hand, scores, am_dealer):
        """ Selects the cards to keep to maximize the net score for those cards
            and the cards in the crib.  Points in the crib count toward the
            total if this policy is the dealer and against the total otherwise.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        crib = 1 if am_dealer else -1
        def score_split(indices):
            keep = []
            throw = []
            for i in range(len(hand)):
                if i in indices:
                    throw.append(hand[i])
                else:
                    keep.append(hand[i])
            throw_score = self.table_get(throw[0].rank(), throw[1].rank(), am_dealer)
            return keep, throw, scoring.score(self._game, keep, None, False)[0] + crib * throw_score
        throw_indices = list(combinations(range(6), 2))
        random.shuffle(throw_indices)
        keep, throw, _ = max(map(score_split, throw_indices), key=lambda t: t[2])
        return keep, throw
    