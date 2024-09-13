import random
from policy import PegPolicy              


class MyPegger(PegPolicy):
    """ My cribbage pegging policy.

    """
    def __init__(self, game):
        super().__init__(game)


    def get_prev_card(self, history):
        """
        get previous card to check for consecutive cards
        """
        prev_card = None
        curr = history
        while prev_card is None:
            if curr._prev_play:
                prev_card = curr._prev_play._card
                curr = curr._prev_play
            else:
                break
        return prev_card
     
    
    def get_pair(self, cards):
        """
        return card you have the most of, minimum being a pair
        """
        card_count = {}
        for card in cards:
            card_count[card.rank()] = card_count.get(card.rank(), 0) + 1            
        paired_cards_count = [(card, card_count[card.rank()]) for card in cards if card_count[card.rank()] >= 2]
        if paired_cards_count:
            return max(paired_cards_count, key=lambda t: t[1])[0]
        else:
            return None            
    

    def peg(self, cards, history, turn, scores, am_dealer):
        """ 
            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            turn -- the cut card
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """  
        # special strategy for leading
        if history.is_start_round():
            self.turns = 0
            # lead with a card from a pair if possible, unless it's a 5
            playable_cards = [card for card in cards if card.rank() != 5]
            paired_card = self.get_pair(playable_cards)
            if paired_card is not None:
                return paired_card

            # play cards in order of priority
            priority = [4, 3, 2, 1, 8, 7, 6, 9, 10, 5]
            for rank in priority:
                for card in cards:
                    if min(card.rank(), 10) == rank:
                        return card

        # greedy strategy: score as high as possible
        # adjust score to apply changes to strategy
        random.shuffle(cards)
        best_card = None
        best_score = None
        prev_card = self.get_prev_card(history)
        for card in cards:
            score = history.score(self._game, card, 0 if am_dealer else 1)
            if score is None:
                continue
            value = score

            # adjust score to reflect desirable totals to reach
            points = history.total_points()        
            total = points + score
            if 22 <= total <= 31:
                value += 0.2 / (32 - total)
            elif total == 21:
                value -= 0.1
            elif 16 <= total <= 20:
                value += 0.02
            elif total == 5:
                value -= 0.1

            # check for pairs
            for other_card in cards:
                if card.rank() == other_card.rank() and card.suit() == other_card.suit():
                    continue
                if card.rank() == other_card.rank():
                    value += 0.2

            # check for cards that can potentially form runs
            above = False
            below = False
            above2 = False
            below2 = False
            for other_card in cards:
                if card.rank() + 1 == other_card.rank():
                    above = True  
                elif card.rank() + 2 == other_card.rank():     
                    above2 = True             
                elif card.rank() - 1 == other_card.rank():
                    below = True
                elif card.rank() - 2 == other_card.rank():
                    below2 = True
            if above:
                value += 0.05
            if above2:
                value += 0.025
            if below:
                value += 0.05
            if below2:
                value -= 0.025

            # if no cards to counter a run, avoid playing cards that threaten runs
            if prev_card is not None:
                if card.rank() + 1 == prev_card.rank() and not (above2 or below2):
                    value -= 0.1
                elif card.rank() - 1 == prev_card.rank() and not (above2 or below2):
                    value -= 0.1                    

            if best_score is None or value > best_score:
                best_score = value
                best_card = card

        return best_card                  

