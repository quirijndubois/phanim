from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from .screen import *
from .functions import *
from .ui import *
from .phobject import *
from .field import *
from .particles import *
from .animate import *
from .curve import *
from .shapes import *
from .group import *
from .color import *
print("phanim imported!")
