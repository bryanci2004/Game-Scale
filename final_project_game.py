from dataclasses import dataclass
from designer import *

# from random import randint

USER_SPEED = 5
WORLD_IMAGE = background_image('Final_Crumbled_background.jpg')
CHARACTER_PLAYER = image('running_stick_man.png')


# ----------------------------------------------------------------------------------------#
@dataclass
class UserPlayer:
    character: DesignerObject
    moving_right: bool
    moving_left: bool
    moving_up: bool
    moving_down: bool


@dataclass
class World:
    main_character: UserPlayer


# ----------------------------------------------------------------------------------------#
def create_world() -> World:
    return World(create_character(image('running_stick_man.png')))


def create_character(character_image: DesignerObject) -> UserPlayer:
    """ Create Player Image """
    # World is first initiated here with the field it needs
    return UserPlayer(character_image, False, False, False, False)


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
        move_character_vertical(world.main_character, -USER_SPEED)
    if world.main_character.moving_down:
        move_character_vertical(world.main_character, USER_SPEED)


def move_character_vertical(user_character: UserPlayer, character_speed: int):
    user_character.character.y += character_speed


def move_character_horizontal(user_character: UserPlayer, character_speed: int):
    user_character.character.x += character_speed


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
when('starting', create_world)
when('typing', press_moving_keys)
when('done typing', release_moving_keys)
when('updating', handle_movement)

start()
