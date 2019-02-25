import gym
import pytest

from gym import error

from leduc.environment import LeducEnv, State, Street, Card, Move

def test_check_folding():
    env = _create_env()
    assert not env is None
    s = env.reset()
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
    assert s[State.BOARD] == Card.BLANK
    assert s[State.BUTTON] == 1
    assert s[State.POT] == 2
    assert s[State.STREET] == Street.PREFLOP
    assert s[State.TO_ACT_POS] == 1
    assert s[State.TO_CALL] == 0
    assert s[State.CARD] in [Card.JACK, Card.QUEEN, Card.KING]
    assert env._players[0].stack == -1 and env._players[1].stack == -1


def _create_env():
    return gym.make('Leduc-v0')