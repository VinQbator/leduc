from enum import IntEnum


class Street(IntEnum):
    PREFLOP = 0
    FLOP = 1
    SHOWDOWN = 2


class Move(IntEnum):
    CHECK = 0
    CALL = 1
    RAISE = 2
    FOLD = 3


class State(IntEnum):
    CARD = 0
    BOARD = 1
    POT = 2
    TO_CALL = 3
    BUTTON = 4
    STREET = 5


class Card(IntEnum):
    JACK = 0
    QUEEN = 1
    KING = 2
    BLANK = 3


def get_safe_action(state, action):
    """
    Return a legal action based on current observed state.
    Changes to best fitting action if current one not valid.
    """

    street = state[State.STREET]
    to_call = state[State.TO_CALL]

    if action == Move.CHECK:
        if to_call != 0:
            return Move.FOLD
    elif action == Move.CALL:
        if to_call == 0:
            return Move.CHECK
    elif action == Move.RAISE:
        if to_call >= 2 * (2 if street == Street.PREFLOP else 4):
            return Move.CALL
    elif action == Move.FOLD:
        if to_call == 0:
            return Move.CHECK
    return action
