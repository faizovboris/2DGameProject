"""Module, containing game configurations."""
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

SKY_COLOR = (25, 156, 255)
TEXT_COLOR = (255, 255, 255)
TEXT_BACKGROUND_COLOR = (255, 100, 100)

BRICK_SIZE = 40
GROUND_Y_POSITION = SCREEN_HEIGHT - BRICK_SIZE * 3 // 2
MAX_LEVEL_WIDTH = 8000

CAT_MAX_X_SPEED = 360
CAT_MAX_Y_SPEED = 360
CAT_WALK_ACCELERATION = 300
CAT_CHANGE_DIRECTION_ACCELERATION = 600
CAT_JUMP_SPEED = -300
CAT_ENEMY_KILLING_JUMP_SPEED = -600
GRAVITY = 700
JUMP_GRAVITY = 300
CAT_SPEED_ZERO_EPS = 5

SCORE_POSITION = (50, 50)
LIVES_POSITION = (600, 50)
