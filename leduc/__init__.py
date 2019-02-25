# -*- coding: utf-8 -*-
from gym.envs.registration import register

from .environment import LeducEnv

register(
 	id='Leduc-v0',
 	entry_point='leduc.environment:LeducEnv',
  kwargs={},
)