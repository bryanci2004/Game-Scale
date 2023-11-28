from dataclasses import dataclass
from designer import *
# from random import randint

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
CENTER_DOT = circle('red', 3, 30, 12)


# ----------------------------------------------------------------------------------------#

@dataclass
class Player:
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
    main_character: Player
    center_dot: DesignerObject
    powerup: list[DesignerObject]
    pause_button: Button


@dataclass
class PauseScreen:
    header: DesignerObject
    resume_button: Button
# ----------------------------------------------------------------------------------------#


def make_button(message: str, x: int, y: int) -> Button:
    horizontal_padding = 4
    vertical_padding = 2
    label = text("black", message, 20, x, y, layer='top')
    return Button(rectangle("lightgreen", label.width + horizontal_padding, label.height + vertical_padding, x, y),
                  rectangle("black", label.width + horizontal_padding, label.height + vertical_padding, x, y, 1),
                  label)


# ----------------------------------------------------------------------------------------#
def create_pause_screen():
    return PauseScreen(text("black", "Pause", 40),
                       make_button("Resume", get_width() / 2, 400))


def handle_world_buttons(world: World):
    """
    The push_scene(scene_name) function can be used to push a new scene onto the stack. Unlike change_scene,
    this will not destroy the current scene, but instead will pause it. When the new scene is popped, the old
    scene will be resumed. In this case, we push the pause screen onto the stack, and pass in the current
    settings as a parameter. Then, when the pause screen is popped, we can resume the overworld with the
    updated settings.
    """
    if colliding_with_mouse(world.pause_button.background):
        push_scene('pause')


def handle_pause_screen_buttons(world: PauseScreen):
    """
    The pop_scene() function can be used to pop the current scene off the stack. This will destroy the current
    scene, and resume the previous scene. In this case, we pop the pause screen off the stack, and pass in the
    chosen_index as a parameter. Then, when the overworld is resumed, we can update the player's avatar.
    Technically, we don't have to pass in the chosen_index, since the settings are already passed in, but
    it's good practice to pass in any parameters that you want to use in the next scene.
    """
    if colliding_with_mouse(world.resume_button.background):
        pop_scene()


# ----------------------------------------------------------------------------------------#
def create_world() -> World:
    return World(create_character(CHARACTER_PLAYER), CENTER_DOT, [], make_button("Pause", 30, 12))


def create_character(character_image: DesignerObject) -> Player:
    """ Create Player Image """
    # World is first initiated here with the field it needs
    return Player(character_image, False, False, False, 0, 0, 0)


# ----------------------------------------------------------------------------------------#

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


def move_character_horizontal(user_character: Player, character_speed: int):
    user_character.moving_speed = character_speed
    user_character.character.x += user_character.moving_speed


def handle_movement(overworld: World):
    instance_y = 0
    if overworld.main_character.moving_right:
        overworld.main_character.character.flip_x = False
        move_character_horizontal(overworld.main_character, MOVING_SPEED)
    if overworld.main_character.moving_left:
        overworld.main_character.character.flip_x = True
        move_character_horizontal(overworld.main_character, -MOVING_SPEED)
    if overworld.main_character.moving_up:
        if overworld.main_character.moving_up_int == 0:
            overworld.main_character.moving_up_int += 1
            if overworld.main_character.moving_up_int == 1:
                jumping_action(overworld, overworld.main_character.character.y)
                overworld.main_character.moving_up_int += 1
    '''
        if world.main_character.moving_up_int == 2:
        instance_y = world.main_character.character.y
        check_user_height(world, instance_y)
        world.main_character.moving_up_int = 0
    '''


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


when('starting: world', create_world)
when('clicking: world', handle_world_buttons)
when('starting: pause', create_pause_screen)
when('clicking: pause', handle_pause_screen_buttons)
when('typing: world', press_moving_keys)
when('typing: world', make_powerup)
when('done typing: world', release_moving_keys)
when('updating: world', handle_movement)
when('updating: world', border_restraining)
when('clicking: world', clicking_coordinate)
when('clicking: pause', handle_pause_screen_buttons)
# when('updating', make_powerup)

start()
