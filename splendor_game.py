# So we will need to build an actual game loop to have the bot self-play
# This will probably involve modelling the game
# I dont actually know if Python is a good choice of language for this. It might be too slow
# The advantages of Python are that we can easily set up a NN and use ML libraries. But are we really going to use ML libraries?

# What is our strategy?
# We could go for a search based system, but given the state space (something like 99 possible cards, 18 showing at once) 
# we could potentially have a huge state space.
# I kind of want to experiment with RL based and Counter Factual Regret minimization approaches

# What are the differences between the two?
# If we use a search based approach, we need a way to evaluate the board state. But as is clear by the fact I am losing at this game
# again and again, I do not have a good system for evaluating the board state.
# I guess lets start by coding up the game. We could do it in a different language from Python and then export the data from the board state.
import csv
import random

LEVEL = 0
COST = slice(1, 6)
POINTS = 6
GEM_REWARD = slice(7, 12)
TOTAL_COST = 12
POINT_REWARD = 13

class Card:
    def __init__(self, level, costs, points, rewards):
        self.level = level
        self.costs = costs
        self.points = points
        self.rewards = rewards

class Player:
    def __init__(self):
        self.hand = list()
        self.wallet = [0] * 6
        self.reserved = list()
        self.score = 0

    def collect_production(self):
        production = [0] * 6
        for card in self.hand:
            for index in range(card.rewards):
                production[index] += card.rewards[index]
        
        return production

    def can_afford(self, card: Card):
        current_gold = self.wallet[-1]
        current_production = self.collect_production()

        for index in len(card.costs):
            if (card.costs[index] > self.wallet[index] + current_production[index] + current_gold):
                return False
        
        return True

    def buy_card(self, card: Card):
        current_production = self.collect_production()
        to_return = [0] * 6
        # Ignore the gold index
        for index in len(self.wallet) - 1:
            spend = card.costs[index] - current_production[index]
            self.wallet[index] -= spend
            to_return[index] = spend
            # balance using gold
            while (self.wallet[index] < 0 and self.wallet[-1] > 0):
                self.wallet[index] += 1
                self.wallet[-1] -= 1
                to_return[-1] += 1
        
        self.hand.append(card)
        self.score += card.points
        return to_return


# gems in order White ,Blue ,Green ,Red ,Black, Gold
class Bank:
    def __init__(self, initial_stack):
        self.gems = [initial_stack] * 6
        # Always 5 gold
        self.gems[5] = 5

class Board:
    def __init__(self, input_tier_1, input_tier_2, input_tier_3, input_nobles, num_players):
        self.tier_1 = input_tier_1
        self.tier_2 = input_tier_2
        self.tier_3 = input_tier_3

        self.state = [list(), list(), list()]
        start = range(0,5)
        for i in start:
            self.state[0].append(self.tier_1.pop(i))

        for i in start:
            self.state[1].append(self.tier_2.pop(i))

        for i in start:
            self.state[2].append(self.tier_3.pop(i))

        self.nobles = list()
        for i in range(0, num_players + 1):
            self.nobles.append(input_nobles[i])

def parse_deck():
    tier_1 = list()
    tier_2 = list()
    tier_3 = list()
    nobles = list()

    with open('splendor_cards.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            card = create_card(row)
            if (card.level == 1):
                tier_1.append(card)
            elif (card.level == 2):
                tier_2.append(card)
            elif (card.level == 3):
                tier_3.append(card)
            elif (card.level == 'Noble'):
                nobles.append(card)

    return tier_1, tier_2, tier_3, nobles

def create_card(row):
    return Card(
        map_level(row[LEVEL]),
        map_cost(row[COST]),
        int(row[POINTS]) if row[POINTS].isdigit()  else 0,
        map_cost(row[COST])
    )

def map_level(level):
    if (level == 'I'):
        return 1
    elif (level == 'II'):
        return 2
    elif (level == 'III'):
        return 3
    elif (level == 'Noble'):
        return 'Noble'

def map_cost(costs):
    mapped = list()
    for cost in costs:
        if (cost.isdigit()):
            mapped.append(int(cost))
        else:
            mapped.append(0)
    return mapped

def main():
    tier_1, tier_2, tier_3, nobles = parse_deck()
    print(len(tier_1))
    print(len(tier_2))
    print(len(tier_3))
    print(len(nobles))

    # Setup game
    random.shuffle(tier_1)
    random.shuffle(tier_2)
    random.shuffle(tier_3)
    random.shuffle(nobles)
    
    num_players = 2
    board = Board(input_tier_1=tier_1, input_tier_2=tier_2, input_tier_3=tier_3, input_nobles=nobles, num_players=num_players)
    bank = Bank(4)
    players = list(Player(), Player())





if __name__ == '__main__':
    main()
