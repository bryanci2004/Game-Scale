from dataclasses import dataclass
from designer import *
from random import randint

'''
Y_GRAVITY = 1
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT
'''
MOVING_SPEED = 7
JUMPING_HEIGHT = 100
GRAVITY = 1
Y_VELOCITY = 200
starting_pos_x, starting_pos_y = 75, 502  # This is for the character

BIGGER_POWER_UP_IMAGE = image('magnify_power_up_transparent.png')
WORLD_IMAGE = background_image('Final_Crumbled_background.jpg')
CHARACTER_PLAYER = image('running_stick_man.png', starting_pos_x, starting_pos_y)
CENTER_DOT = circle('red', 3, 200, 400)


# ----------------------------------------------------------------------------------------#
@dataclass
class UserPlayer:
    character: DesignerObject
    moving_right: bool
    moving_left: bool
    moving_up: bool
    moving_up_int: int
    moving_speed: int
    jumping_speed: int


@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject


@dataclass
class World:
    main_character: UserPlayer
    center_dot: DesignerObject
    powerup: list[DesignerObject]
    pause_button: Button


@dataclass
class PauseScreen:
    header: DesignerObject
    resume_button: Button
    cursor: DesignerObject


def make_button(message: str, x: int, y: int) -> Button:
    horizontal_padding = 4
    vertical_padding = 2
    label = text("black", message, 20, x, y, layer='top')
    return Button(rectangle("lightgreen", label.width + horizontal_padding, label.height + vertical_padding, x, y),
                  rectangle("black", label.width + horizontal_padding, label.height + vertical_padding, x, y, 1),
                  label)


def create_pause_screen():
    return PauseScreen(text("black", "Pause", 40),
                       make_button("Resume", get_width() / 2, 400),
                       rectangle("black", 32, 32))


# ----------------------------------------------------------------------------------------#
def create_world() -> World:
    return World(create_character(CHARACTER_PLAYER), CENTER_DOT, [], make_button("Pause", 30, 12))


def create_character(character_image: DesignerObject) -> UserPlayer:
    """ Create Player Image """
    # World is first initiated here with the field it needs
    return UserPlayer(character_image, False, False, False, 0, 0, 0)


# ----------------------------------------------------------------------------------------#
def handle_movement(world: World):
    instance_y = 0
    if world.main_character.moving_right:
        world.main_character.character.flip_x = False
        move_character_horizontal(world.main_character, MOVING_SPEED)
    if world.main_character.moving_left:
        world.main_character.character.flip_x = True
        move_character_horizontal(world.main_character, -MOVING_SPEED)
    if world.main_character.moving_up:
        if world.main_character.moving_up_int == 0:
            world.main_character.moving_up_int += 1
            if world.main_character.moving_up_int == 1:
                jumping_action(world, world.main_character.character.y)
                world.main_character.moving_up_int += 1
    '''
        if world.main_character.moving_up_int == 2:
        instance_y = world.main_character.character.y
        check_user_height(world, instance_y)
        world.main_character.moving_up_int = 0
    '''


def check_user_height(world: World, check_y: int):
    if world.main_character.character.y < check_y:
        glide_down(world.main_character.character, JUMPING_HEIGHT)


def jumping_action(world: World, previous_y: int):
    if world.main_character.character.y > previous_y - 20:
        glide_up(world.main_character.character, JUMPING_HEIGHT)


def release_moving_keys(world: World, key: str):
    main_character = world.main_character
    """When either right/left key is let go of, the character will stop moving that direction"""
    if key == 'right':
        main_character.moving_right = False
    if key == 'left':
        main_character.moving_left = False


def press_moving_keys(world: World, key: str):
    """Depending on the type of left/right arrow pressed, the character will move that direction while holding"""
    if key == 'right':
        world.main_character.moving_right = True
    if key == 'left':
        world.main_character.moving_left = True
    if key == 'space':
        world.main_character.moving_up = True


def move_character_horizontal(user_character: UserPlayer, character_speed: int):
    user_character.moving_speed = character_speed
    user_character.character.x += user_character.moving_speed


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

    if world.main_character.character.y > 500:
        world.main_character.jumping_speed = -world.main_character.jumping_speed
        world.main_character.character.y += world.main_character.jumping_speed


# ----------------------------------------------------------------------------------------#
def create_power_up() -> DesignerObject:
    power_up = BIGGER_POWER_UP_IMAGE
    power_up.x = 200
    power_up.y = 300
    return power_up


def make_powerup(world: World, key: str):
    world_list_powerup = world.powerup
    if key == 'j':
        world_list_powerup.append(create_power_up())
        world.powerup = world_list_powerup
        print(world.powerup)


'''
def make_powerup(world: World, key: str):
    if key == 'j':
        world.powerup.append(create_power_up())
        print(world.powerup)
'''


def clicking_coordinate(x: int, y: int):
    print('X Coordinate:', str(x))
    print('Y Coordinate:', str(y))


when('starting', create_world)
when('starting: pause', create_pause_screen)
when('typing', press_moving_keys)
when('typing', make_powerup)
when('done typing', release_moving_keys)
when('updating', handle_movement)
when('updating', border_restraining)
when('clicking', clicking_coordinate)
# when('updating', make_powerup)

start()
