"""
Created on: 8-2-2018
@author: Stef
"""
import itertools
import numpy as np
import os

# GAME SETTINGS
HUMAN_PLAYER = False
RUN_IN_PARALLEL = True

GAME_SIZE = 1 if not HUMAN_PLAYER else 3
STEP_SIZE = 5 * GAME_SIZE
LENGTH = 3
DISPLAY_WIDTH = 100 * GAME_SIZE
DISPLAY_HEIGHT = 100 * GAME_SIZE
RASTER_SIZE = DISPLAY_WIDTH // STEP_SIZE * DISPLAY_HEIGHT // STEP_SIZE
BOUNDARY = False

x_list = list(range(0, DISPLAY_WIDTH + STEP_SIZE, STEP_SIZE))
y_list = list(range(0, DISPLAY_HEIGHT + STEP_SIZE, STEP_SIZE))
COORDINATES = list(itertools.product(x_list, y_list))
COORDINATES_BOUNDARY = [(-STEP_SIZE, c) for c in y_list]
COORDINATES_BOUNDARY.extend([(DISPLAY_WIDTH, c) for c in y_list])
COORDINATES_BOUNDARY.extend([(c, -STEP_SIZE) for c in y_list])
COORDINATES_BOUNDARY.extend([(c, DISPLAY_HEIGHT) for c in y_list])
FRAME_RATE = 50 / 500  # if HUMAN_PLAYER else None
SCREENS_PER_ROW = 10

# NEUROEVOLUTION SETTINGS
STEP_LIMIT = np.inf if HUMAN_PLAYER else 200
GENERATIONS = 50
EAT_APPLE_SCORE = 100
APPROACHING_SCORE = 1
RETRACTING_PENALTY = 1.5
COLLISION_PENALTY = 1000

# OUTPUT SETTINGS
PATH_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_INPUT = os.path.join(PATH_HOME, "input")
PATH_OUTPUT = os.path.join(PATH_HOME, "output")
PATH_OUTPUT_TEMP = os.path.join(PATH_OUTPUT, "temp")
