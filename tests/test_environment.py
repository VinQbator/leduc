import gym
import pytest

import numpy as np
from gym import error

from leduc.environment import LeducEnv, State, Street, Card, Move
from leduc.util import get_safe_action

def test_check_folding():
    env = _create_env()
    assert not env is None
    s = env.reset()
    s = s['state']
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 0
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1

    # BTN check
    s, r, d, i = env.step(Move.CHECK)
    s = s['state']
    assert r == [0, 0]
    assert d == False
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1

    # BB bet
    s, r, d, i = env.step(Move.RAISE)
    s = s['state']
    assert r == [0, 0]
    assert d == False
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 4
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 0
    assert s[State.TO_CALL] == 2
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -3

    # BTN fold
    s, r, d, i = env.step(Move.FOLD)
    s = s['state']
    assert r == [-1, 1]
    assert d == True
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 4
    assert s[State.STREET] == Street.SHOWDOWN
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 2
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == 1

    s = env.reset()
    s = s['state']
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 1
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1

def test_showdown():
    env = _create_env()
    assert not env is None
    s = env.reset()
    s = s['state']
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 0
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1

    # BTN bet
    s, r, d, i = env.step(Move.RAISE)
    s = s['state']
    assert r == [0, 0]
    assert d == False
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 4
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 2
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -3 and env._players[1].stack == -1

    # BB call
    s, r, d, i = env.step(Move.CALL)
    s = s['state']
    assert r == [0, 0]
    assert d == False
    assert s[State.BOARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 6
    assert s[State.STREET] == Street.FLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -3 and env._players[1].stack == -3

    # BB bet
    s, r, d, i = env.step(Move.RAISE)
    s = s['state']
    assert r ==  [0, 0]
    assert d == False
    assert s[State.BOARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 10
    assert s[State.STREET] == Street.FLOP
    assert s[State.TO_ACT_POS] == 0
    assert s[State.TO_CALL] == 4
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -3 and env._players[1].stack == -7

    # BTN raise
    s, r, d, i = env.step(Move.RAISE)
    s = s['state']
    assert r == [0, 0]
    assert d == False
    assert s[State.BOARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 18
    assert s[State.STREET] == Street.FLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 8
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -11 and env._players[1].stack == -7

    # BB call
    s, r, d, i = env.step(Move.CALL)
    s = s['state']
    assert sum(r) == 0
    assert d == True
    assert s[State.BOARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert s[State.BUTTON] == 0
    assert s[State.POT] == 22
    assert s[State.STREET] == Street.SHOWDOWN
    assert s[State.TO_ACT_POS] == 0
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -env._players[1].stack

    exception_raised = False
    try:
        env.step(Move.CHECK)
    except error.Error:
        exception_raised = True
    assert exception_raised

    s = env.reset()
    s = s['state']
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 1
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1

def test_safe_actions():
    env = _create_env()
    i = 0
    done = True
    state = None
    while i < 1000:
        i += 1
        if done:
            state = env.reset()
        state, _, done, _ = env.step(get_safe_action(state, np.random.randint(0, 4)))



# Private methods
def _create_env():
    return gym.make('Leduc-v0')