from dataclasses import dataclass
from designer import *
from random import randint

USER_SPEED = 15
WORLD_IMAGE = background_image('game_background.png')
CHARACTER_PLAYER = image('running_stick_man.png')


@dataclass
class UserPlayer:
    Character: DesignerObject
    Moving: bool


@dataclass
class World:
    Character: UserPlayer


def create_character(character_image: DesignerObject) -> UserPlayer:
    """ Create Player Image """
    # World is first initiated here with the field it needs
    return UserPlayer(character_image)


def create_world() -> World:
    return World(create_character(image('running_stick_man.png')))


def continuous_movement_around(user_character: UserPlayer):
    user_character.Moving = True


def stop_continuous_movement_around(user_character: UserPlayer):
    user_character.Moving = False





print(get_height())
print(get_width())
when('starting', create_world)
when('typing', continuous_movement_around)

start()
