import numpy as np

from gym import Env, error, spaces, utils
from gym.utils import seeding

from leduc.util import Street, Move, State, Card

class Player():
    def __init__(self):
        self.stack = 0
        self.card = None
    
    def reset(self, card):
        self.stack = -1
        self.card = card

class Deck():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._cards = [Card.JACK, Card.JACK, Card.QUEEN, Card.QUEEN, Card.KING, Card.KING]

    def draw(self):
        card = np.random.choice(self._cards, 1)
        self._cards.remove(card)
        return card[0]

class LeducEnv(Env):
    def __init__(self):
        self._button = -1
        self._players = [Player(), Player()]
        self._street = Street.PREFLOP
        self._pot = 0
        self._to_call = 0
        self._deck = Deck()
        self._board = Card.BLANK

        self.observation_space = spaces.MultiDiscrete([3, 4, 27, 5, 2, 2, 3])
        self.action_space = spaces.Discrete(4)

    def reset(self):
        self._button = (self._button + 1) % 2
        self._to_act = self._button
        self._current_player = self._players[self._to_act]
        self._street = Street.PREFLOP
        self._deck.reset()
        for player in self._players:
            player.reset(self._deck.draw())
        self._board = Card.BLANK
        self._pot = 2
        self._to_call = 0
        
        return self._state

    def step(self, action):
        if not self._street < Street.SHOWDOWN:
            raise error.Error('Reset the environment after hand ended!')

        street_done = False
        if action == Move.CHECK:
            assert self._to_call == 0
            if (self._street == Street.PREFLOP and self._to_act != self._button)\
                or (self._street == Street.FLOP and self._to_act == self._button):
                street_done = True
        elif action == Move.CALL:
            assert self._to_call > 0
            self._pot += self._betsize
            self._current_player.stack -= self._betsize
            street_done = True
        elif action == Move.RAISE:
            assert self._to_call < 2 * self._betsize
            addition_to_pot = self._to_call + self._betsize
            self._pot += addition_to_pot
            self._current_player.stack -= addition_to_pot
            self._to_call += self._betsize
        elif action == Move.FOLD:
            assert self._to_call > 0
            self._players[(self._to_act + 1) % 2].stack += self._pot
            self._street = Street.SHOWDOWN

        self._to_act = (self._to_act + 1) % 2
        self._current_player = self._players[self._to_act]

        if street_done:
            self._street += 1
            if self._street == Street.FLOP:
                self._board = self._deck.draw()
                self._to_act = (self._button + 1) % 2
                self._current_player = self._players[self._to_act]
                self._to_call = 0
            elif self._street == Street.SHOWDOWN:
                winners = self._showdown()
                prize = self._pot / len(winners)
                for p in winners:
                    p.stack += prize
            else:
                raise Exception('Should never happen')
            self._to_call = 0
        
        reward = [0, 0]
        if self._street == Street.SHOWDOWN:
            reward = [p.stack for p in self._players]
        state = self._state
        info = {}
        done = self._street == Street.SHOWDOWN

        return state, reward, done, info

    def render(self):
        print('Board %s, Pot, %s, To Call %s, Next To Act %s' % (self._board, self._pot, self._to_call, self._to_act))
        i = 0
        for p in self._players:
            print('Player %s, Card %s, Total Bet %s' % (str(i), str(p.card), str(-p.stack)))
            i += 1

    @property
    def _betsize(self):
        return 2 if self._street == Street.PREFLOP else 4

    @property
    def _state(self):
        return (int(self._current_player.card), int(self._board), self._pot, self._to_call, self._to_act, self._button, int(self._street))

    def _showdown(self):
        winning_hand = max([self._evaluate_hand(p.card) for p in self._players])
        winners = [p for p in self._players if self._evaluate_hand(p.card) == winning_hand]
        return winners

    def _evaluate_hand(self, card):
        return int(card) if card != self._board else int(card) + 3
