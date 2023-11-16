from dataclasses import dataclass
from designer import *

# from random import randint

USER_SPEED = 3
WORLD_IMAGE = background_image('Final_Crumbled_background.jpg')
CHARACTER_PLAYER = image('running_stick_man.png', 75, 502)
CENTER_DOT = circle('red', 3, 86, 473)
GRAVITY = 3
JUMPING_SPEED = 3


# ----------------------------------------------------------------------------------------#
@dataclass
class UserPlayer:
    character: DesignerObject
    moving_right: bool
    moving_left: bool
    moving_up: bool
    moving_down: bool
    moving_speed: int
    jumping_speed: int


@dataclass
class World:
    main_character: UserPlayer
    center_dor: DesignerObject


# ----------------------------------------------------------------------------------------#
def create_world() -> World:
    return World(create_character(CHARACTER_PLAYER), CENTER_DOT)


def create_character(character_image: DesignerObject) -> UserPlayer:
    """ Create Player Image """
    # World is first initiated here with the field it needs
    return UserPlayer(character_image, False, False, False, False, 0, 0)


# ----------------------------------------------------------------------------------------#
def press_moving_keys(world: World, key: str):
    """Depending on the type of left/right arrow pressed, the character will move that direction while holding"""
    if key == 'right':
        horizontal_right_move(world.main_character)
    if key == 'left':
        horizontal_left_move(world.main_character)
    if key == 'up':
        vertical_move_up(world.main_character)
    if key == 'down':
        vertical_move_down(world.main_character)


def release_moving_keys(world: World, key: str):
    """When either right/left key is let go of, the character will stop moving that direction"""
    if key == 'right':
        stop_horizontal_right_move(world.main_character)
    if key == 'left':
        stop_horizontal_left_move(world.main_character)
    if key == 'up':
        stop_vertical_move_up(world.main_character)
    if key == 'down':
        stop_vertical_move_down(world.main_character)


def handle_movement(world: World):
    if world.main_character.moving_right:
        world.main_character.character.flip_x = False
        move_character_horizontal(world.main_character, USER_SPEED)
    if world.main_character.moving_left:
        world.main_character.character.flip_x = True
        move_character_horizontal(world.main_character, -USER_SPEED)
    if world.main_character.moving_up:
        move_character_vertical(world.main_character, -JUMPING_SPEED)
    if world.main_character.moving_down:
        move_character_vertical(world.main_character, JUMPING_SPEED)


def move_character_vertical(user_character: UserPlayer, character_speed: int):
    user_character.jumping_speed = character_speed
    user_character.character.y += user_character.jumping_speed


def move_character_horizontal(user_character: UserPlayer, character_speed: int):
    user_character.moving_speed = character_speed
    user_character.character.x += user_character.moving_speed


def horizontal_right_move(user_character: UserPlayer):
    user_character.moving_right = True


def horizontal_left_move(user_character: UserPlayer):
    user_character.moving_left = True


def vertical_move_up(user_character: UserPlayer):
    user_character.moving_up = True


def vertical_move_down(user_character: UserPlayer):
    user_character.moving_down = True


def stop_horizontal_right_move(user_character: UserPlayer):
    user_character.moving_right = False


def stop_horizontal_left_move(user_character: UserPlayer):
    user_character.moving_left = False


def stop_vertical_move_up(user_character: UserPlayer):
    user_character.moving_up = False


def stop_vertical_move_down(user_character: UserPlayer):
    user_character.moving_down = False


# ----------------------------------------------------------------------------------------#
def showing_coordinates(world: World, x_cor: int, y_cor: int):
    print("X Coordinate: ", str(x_cor))
    print("Y Coordinate: ", str(y_cor))


# ----------------------------------------------------------------------------------------#
def border_restraining(world: World):
    if world.main_character.character.x < 42:
        world.main_character.moving_speed = world.main_character.moving_speed
        world.main_character.moving_left = False
        world.main_character.character.x += -world.main_character.moving_speed

    if world.main_character.character.x > 650:
        world.main_character.moving_speed = -world.main_character.moving_speed
        world.main_character.moving_right = False
        world.main_character.character.x += world.main_character.moving_speed

    if world.main_character.character.y > 502:
        world.main_character.jumping_speed = -world.main_character.jumping_speed
        world.main_character.moving_down = False
        world.main_character.character.y += world.main_character.jumping_speed


'''
def game_gravity(world: World):
    world.main_character.character.y += GRAVITY
'''

when('starting', create_world)
when('typing', press_moving_keys)
when('clicking', showing_coordinates)
when('done typing', release_moving_keys)
when('updating', handle_movement)
#when('updating', game_gravity)
when('updating', border_restraining)

start()
