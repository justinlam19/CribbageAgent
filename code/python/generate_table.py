from itertools import combinations, combinations_with_replacement
import random
import pickle
import sys


def straight_value(length, count):
        if length >= 3:
            return length * count
        else:
            return 0


def score_cards(cards):
    """
    ignores suits for the sake of speed
    """
    rank_count = {rank: 0 for rank in range(1, 14)}
    value_count = {value: 0 for value in range(1, 11)}
    
    for card in cards:
        rank_count[card] += 1
        value_count[min(card, 10)] += 1

    fifteens = 0
    for size in range(2, 6):
        for card_combinations in combinations(cards, size):
            if sum(min(card, 10) for card in card_combinations) == 15:
                fifteens += 1
    fifteens *= 2
        
    pairs = 0
    for r in range(1, 14):
        pairs += len(list(combinations(range(rank_count[r]), 2)))
    pairs *= 2
    
    straights = 0
    curr_run = 0
    combos = 1
    for r in range(1, 14):
        if rank_count[r] == 0:
            straights += straight_value(curr_run, combos)
            curr_run = 0
            combos = 1
        else:
            curr_run += 1
            combos *= rank_count[r]
    straights += straight_value(curr_run, combos)
        
    return pairs + fifteens + straights


def discard(deal, crib):
    """
    mimics greedy strategy of opponent, but ignores suits for the sake of speed
    """
    def score_split(indices):
        keep = []
        throw = []
        for i in range(len(deal)):
            if i in indices:
                throw.append(deal[i])
            else:
                keep.append(deal[i])
        return keep, throw, score_cards(keep) + crib * score_cards(throw)
    throw_indices = list(combinations(range(6), 2))
    random.shuffle(throw_indices)
    return max(map(score_split, throw_indices), key=lambda t: t[2])[1]


def table_set(table, i, j, val):
    table[i - 1][j - 1] = val
    if i != j:
        table[j - 1][i - 1] = val


if __name__ == '__main__':
    check = input("Are you sure? This will overwrite existing discard tables (y/n): ")
    while not (check.lower() == "y" or check.lower() == "n"):
        check = input("Please enter (y/n): ")
    if check.lower() == "n":
        sys.exit(0)

    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
    else:
        # after testing, for score to be approx 0.22 (combined with PegPolicy), we need at least 500,000 iterations
        # the generated table has been run for 2,000,000 iterations
        iterations = 500000

    pairs = combinations_with_replacement(range(1, 14), 2)

    dealer_table = [[0] * 13 for _ in range(13)]
    nondealer_table = [[0] * 13 for _ in range(13)]

    for a, b in pairs:
        possible_cards = [rank for rank in range(1, 14) for _ in range(4)]
        possible_cards.remove(a)
        possible_cards.remove(b)

        dealer_total = 0
        nondealer_total = 0
        for _ in range(iterations):
            cards = random.sample(possible_cards, 6)
            turn, *opponent_deal = cards
            dealer_total += score_cards([a, b] + discard(opponent_deal, crib=1) + [turn])
            nondealer_total += score_cards([a, b] + discard(opponent_deal, crib=-1) + [turn])
        dealer_score = dealer_total / iterations
        nondealer_score = nondealer_total / iterations

        # deal with nob
        if a == 11:
            dealer_score += 0.25
            nondealer_score += 0.25
        if b == 11:
            dealer_score += 0.25
            nondealer_score += 0.25

        table_set(dealer_table, a, b, dealer_score)
        table_set(nondealer_table, a, b, nondealer_score)


    with open('dealer.pkl', 'wb') as f:
        pickle.dump(dealer_table, f)

    with open('nondealer.pkl', 'wb') as f:
        pickle.dump(nondealer_table, f)
