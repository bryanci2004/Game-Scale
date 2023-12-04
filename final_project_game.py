"""[1] - https://www.youtube.com/watch?v=am2Tb_tj8zM (This video helps
teach how to implement jumping into your game clearly. Very useful video)"""

from dataclasses import dataclass
from designer import *
from random import randint

GLOBAL_MOVING_SPEED = 10

WORLD_IMAGE = background_image('LADDER_WORLD_MAP.jpg')

starting_pos_x, starting_pos_y = 75, 494  # This is for the character
CHARACTER_PLAYER_IMAGE = image('running_stick_man.png', starting_pos_x, starting_pos_y)
CHARACTER_PLAYER_IMAGE.scale = .02


# ----------------------------------------------------------------------------------------#
@dataclass
class Player:
    character_image: DesignerObject
    moving_right_bool: bool
    moving_left_bool: bool
    moving_up_bool: bool
    jumping_integer: int
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
    magnifying_glass_list: list[DesignerObject]
    eraser_list: list[DesignerObject]
    tape_list: list[DesignerObject]
    pause_button: Button
    ladder_list: list[DesignerObject]
    crown: DesignerObject


@dataclass
class PauseScreen:
    header: DesignerObject
    resume_button: Button


@dataclass
class GameOverScreen:
    header: DesignerObject
    end_game_button: Button


@dataclass
class WinningScreen:
    header: DesignerObject
    quit_game_button: Button


# ----------------------------------------------------------------------------------------#


def create_world() -> World:
    """
    This function is what starts the entire game. It will create the world
    with all the necessary variables needed.

    Returns:
        World: The world/game
    """
    return World(create_character(CHARACTER_PLAYER_IMAGE), [],
                 [], [],
                 make_button("Pause", 30, 12),
                 [hide(create_ladder_rectangles(577, 453, 146)),
                  hide(create_ladder_rectangles(356, 343, 78)),
                  hide(create_ladder_rectangles(597, 244, 124)),
                  hide(create_ladder_rectangles(235, 121, 128))], emoji('👑', 630, 39))


def create_ladder_rectangles(x_cor: int, y_cor: int, height: int) -> DesignerObject:
    """
    This function creates the invisible rectangles that are
    used for collision in order for the character to know when to climb up
    the ladder. The programmer provides the necessary coordinates and how high
    the rectangle is for the purpose of the game.

    Args:
        x_cor: X coordinate as an integer.
        y_cor: Y coordinate as an integer
        height: Integer of how high the rectangle is

    Returns:
        DesignerObject: Returns as a rectangle with the desired x-coordinate, y-coordinate and height
    """
    return Rectangle('brown', 22, height, x_cor, y_cor)


def create_character(character_image: DesignerObject) -> Player:
    """
    This function creates the 'character' that the user will be playing as. This
    function is meant to be as a helper function.

    Args:
        character_image: The file name of the image that will be used is given here.

    Returns:
        Player: This function returns a dataclass that's given all it's necessary fields
        in order to be displayed in the game.
    """
    return Player(character_image, False, False, False, 0, 0, 0)  # The p


# ----------------------------------------------------------------------------------------#


def make_button(message: str, x: int, y: int) -> Button:
    """
    This function creates the button that is used as pause/resume

    Args:
        message: The function will be given the message/label when called to give the button.
        x: X coordinate as an integer
        y: Y coordinate as an integer

    Returns:
        Button: This function will return a Button dataclass with all the required
        field fulfilled in order to be displayed in the world.
    """

    horizontal_padding = 4
    vertical_padding = 2
    label = text("black", message, 20, x, y, layer='top')
    return Button(rectangle("lightgreen", label.width + horizontal_padding, label.height + vertical_padding, x, y)
                  , rectangle("black", label.width + horizontal_padding, label.height + vertical_padding, x, y,
                              1), label)


# ----------------------------------------------------------------------------------------#
def create_pause_screen() -> PauseScreen:
    """
    This function is a helper function. All it will do is return the PauseScreen dataclass
    which is then returned as a window for the user to see. This will display the message saying the
    game is paused and there will be a resume button.

    Returns:
        PauseScreen: This is the PauseScreen dataclass being returned which will be displayed to the user.
    """
    return PauseScreen(text("black", "Pause", 40),
                       make_button("Resume", get_width() / 2, 400))


def handle_world_pause_button(world: World):
    """
    The push_scene(scene_name) function can be used to push a new scene onto the stack. Unlike change_scene,
    this will not destroy the current scene, but instead will pause it. When the new scene is popped, the old
    scene will be resumed. In this case, we push the pause screen onto the stack, and pass in the current
    settings as a parameter. Then, when the pause screen is popped, we can resume the overworld with the
    updated settings.
    """
    """
    This function is what handles the "pause" button in the world 

    Args:
        world: This function is given the World dataclass

    Returns:
        push_scene: This function is returned which is pushing the 'pause' scene which shows the 
        message showing that the game is paused along with the resume button. 
    """
    if colliding_with_mouse(world.pause_button.background):
        push_scene('pause')


def handle_pause_screen_buttons(pause_screen: PauseScreen):
    """
    The pop_scene() function can be used to pop the current scene off the stack. This will destroy the current
    scene, and resume the previous scene. In this case, we pop the pause screen off the stack, and pass in the
    chosen_index as a parameter. Then, when the overworld is resumed, we can update the player's avatar.
    Technically, we don't have to pass in the chosen_index, since the settings are already passed in, but
    it's good practice to pass in any parameters that you want to use in the next scene.
    """
    """
    This function creates the invisible rectangles that are
    used for collision in order for the character to know when to climb up
    the ladder. The programmer provides the necessary coordinates and how high
    the rectangle is for the purpose of the game.     

    Args:
        pause_screen: This function is given the PauseScreen dataclass

    Returns:
        pop_scene: This function will pop/remove the pause screen window and return the original
        world window/game window. 
    """
    if colliding_with_mouse(pause_screen.resume_button.background):
        pop_scene()


# ----------------------------------------------------------------------------------------#
def create_game_over_screen():
    """
    This function creates the game-over screen.
    """
    return GameOverScreen(text("red", "GAME OVER! Thank you for playing!", 40),
                          make_button("End the Game!", get_width() / 2, 400))


def handle_game_over_screen_buttons(game_over_screen: GameOverScreen):
    """This function handles the game-over screen buttons"""
    if colliding_with_mouse(game_over_screen.end_game_button.background):
        quit()


# ----------------------------------------------------------------------------------------#
def create_winner_screen():
    return WinningScreen(text("green", "Congratulations you win!", 40),
                         make_button("Quit to Desktop", get_width() / 2, 400))


def handle_winner_screen_buttons(winning_screen: WinningScreen):
    if colliding_with_mouse(winning_screen.quit_game_button.background):
        quit()


# ----------------------------------------------------------------------------------------#
def release_moving_keys(world: World, key: str):
    """
    This function handles the keys released by the user. This function works along with the
    'press_moving_keys' function. These two functions work together to make it possible for the user to
    only have to hold the direction in which they want to go instead of having to tap the direction
    button each time they want to move.

    Args:
        world: The World dataclass
        key: The key that the user released is given to this function. This is in the form of a string.

    Returns:
        The function will change the booleans of the character from true to false which in turn will
        stop the character from moving.
    """
    main_character = world.main_character
    if key == 'right':  # Right arrow key
        main_character.moving_right_bool = False
    if key == 'left':  # Left arrow key
        main_character.moving_left_bool = False


def press_moving_keys(world: World, key: str):
    """
    This function is the second part of moving the character. This is the first thing that the user will do.
    The user will press the key which is registered by this function. Depending on the direction of the arrow
    that the user presses will determine which boolean is changed in order to move the
    character in the direction that the user wants to go.

    Args:
        world: The World dataclass
        key: The key that the user presses in the form of a string

    Returns:
        This function changes the boolean of the direction that the user wants to go from False to True to initiate
        the movement.
    """
    main_character = world.main_character
    if key == 'right':  # Right arrow key is pressed down
        main_character.moving_right_bool = True
    if key == 'left':  # Left arrow key is pressed down
        main_character.moving_left_bool = True
    if key == 'space' or key == 'up':  # The user can either press down the up arrow or the space bar to jump.
        main_character.moving_up_bool = True


# ----------------------------------------------------------------------------------------#
def move_character_horizontal(user_character: Player, character_speed: int):
    """
    This is a handler function. This function handles the horizontal movement from the character.
    The function achives this by increasing for decreasing the x-coordinate of the character by increments.

    Args:
        user_character: The Player datalcass is given to this function
        character_speed: The speed at which the character will change.

    Returns:
        This function moves the character either right or left.
    """
    user_character.moving_speed = character_speed
    user_character.character_image.x += user_character.moving_speed

# Global variables for jumping
JUMPING_HEIGHT = 14
GRAVITY = 2


def handle_movement(world: World):
    """
    This is a handler function. This function builds off of the 'press_moving_keys' and 'release_moving_keys'.
    This function is anticipating for the Player dataclass fields which are the moving direction booleans to change.
    Whenever one of the fields turn to true from the 'press_moving_keys', it will move the character using the
    'move_character' function which moves the character through increasing the x-coordinate.

    Args:
        world: The World dataclass
    Returns:
        Will move the character in the corresponding direction.
    """
    global JUMPING_HEIGHT, GRAVITY  # This calls the global variables which handle the jumping feature.
    main_character = world.main_character
    if main_character.moving_right_bool:
        main_character.character_image.flip_x = False
        move_character_horizontal(main_character, GLOBAL_MOVING_SPEED)
    if main_character.moving_left_bool:
        main_character.character_image.flip_x = True
        move_character_horizontal(main_character, -GLOBAL_MOVING_SPEED)
    """[1] - The code below is what handles the jumping action from the character. I used the instructional YouTube
    Video to recreate the jumping into my game."""
    if main_character.moving_up_bool:
        main_character.character_image.y -= JUMPING_HEIGHT
        JUMPING_HEIGHT -= GRAVITY
        if JUMPING_HEIGHT < -14:
            world.main_character.moving_up_bool = False
            JUMPING_HEIGHT = 14


# ----------------------------------------------------------------------------------------#
def border_restraining(world: World):
    """
    This function is meant to restrain the user using borders to prevent the user from going out of the screen.
    This function requires more tinkering to perfect the individual levels since each one is unique.

    Args:
        world: The World dataclass
    Returns:
        Creates invisible borders that restrain the user's movement, so they don't go off the screen.
    """
    character_image = world.main_character.character_image
    character = world.main_character
    if character_image.x < 42:
        character.moving_left_bool = False
        character_image.x += -world.main_character.moving_speed

    if character_image.x > 650:
        character.moving_right_bool = False
        character_image.x += -world.main_character.moving_speed

    if round(character_image.y) > 494:
        world.main_character.character_image.y += 0


# ----------------------------------------------------------------------------------------#
def create_power_up_second_level(image_str: str) -> DesignerObject:
    """
    This is function creates power-ups in random positions at the second level only.
    Args:
        image_str: This is the image/power-up that is consumed by the function in order to
        display it on screen. Since each power-up has its own unique picture, the parameter
        makes the code easier to understand and easy to change at a more broad level.
    Returns:
        The power-up at a random spot at the second level only.
    """
    power_up = image(image_str)
    power_up.scale = .02  # This scales the image down since it's huge normally
    power_up.x = randint(41, 537)
    power_up.y = 368  # Second level y-coordinate
    return power_up


def create_obstacles_third_level(image_string: str) -> DesignerObject:
    """
    This is function creates power-ups in random positions at the third level only.
    Args:
        image_string: This is the image/power-up that is consumed by the function in order to
        display it on screen. Since each power-up has its own unique picture, the parameter
        makes the code easier to understand and easy to change at a more broad level.
    Returns:
        The power-up at a random spot at the third level only.
    """
    obstacle = image(image_string)
    obstacle.scale = .02  # This scales the picture down since it's huge normally
    obstacle.x = randint(263, 654)
    obstacle.y = 43  # Third level y-coordinate
    return obstacle


# ----------------------------------------------------------------------------------------#
def make_powerup_magnifying_glass(world: World):
    """
    This is function creates the Magnifying Glass Power-up(makes character bigger).
    Args:
        world: World dataclass
    Returns:
        Create the magnifying glass power-up which appears in the game but at random times.
    """
    world_glass_list = world.magnifying_glass_list
    glass_list_length = len(world_glass_list)
    if randint(0, 20) == 7 and glass_list_length < 2:
        world_glass_list.append(create_power_up_second_level('magnify_power_up_transparent.png'))
        world.magnifying_glass_list = world_glass_list


def make_powerup_eraser(world: World):
    """
    This is function creates the Eraser Power-up(makes character smaller).
    Args:
        world: World dataclass
    Returns:
        Create the eraser power-up which appears in the game but at random times.
    """
    world_eraser_list = world.eraser_list
    eraser_list_length = len(world_eraser_list)
    if randint(0, 20) == 10 and eraser_list_length < 2:
        world_eraser_list.append(create_power_up_second_level('new_eraser.png'))
        world.eraser_list = world_eraser_list


def make_tape_obstacle(world: World):
    """
    This is function creates the tape obstacle(makes user 'die').
    Args:
        world: World dataclass
    Returns:
        Create the tape obstacle which appears in the game but at random times.
    """
    world_list_tape = world.tape_list
    tape_list_length = len(world_list_tape)
    if randint(1, 8) == 7 and tape_list_length < 5:
        world_list_tape.append(create_random_tape_obstacles('new_tape.png'))
        world.tape_list = world_list_tape


def create_random_tape_obstacles(image_string: str):
    """
    This is function will determine where the random tape obstacle will spawn. There are 5 different levels to the game.
    Whichever random level gets chosen is where the tape will spawn.
    Args:
        image_string: The string name of the picture of the tape that will display to the user.
    Returns:
        This function will display the tape obstacles in random spots throughout the game.
    """
    obstacle = image(image_string)
    obstacle.scale = .02
    magic_number = randint(1, 5)
    if magic_number == 1:
        obstacle.x = randint(120, 553)
        obstacle.y = 528
        return obstacle
    if magic_number == 2:
        obstacle.x = randint(378, 530)
        obstacle.y = 382
        return obstacle
    if magic_number == 3:
        obstacle.x = 548
        # obstacle.x = randint(400, 548)
        obstacle.y = 305
        return obstacle
    if magic_number == 4:
        obstacle.x = randint(267, 545)
        obstacle.y = 185
        return obstacle
    if magic_number == 5:
        obstacle.x = randint(295, 654)
        obstacle.y = 60
        return obstacle


def teleport_obstacles(world: World):
    """
    I didn't have the time to implement moving tape obstacles. But I decided to come up with a different idea that
    makes the game more fun. The tape obstacles will randomly spawn in random spots.
    Args:
        world: The World Dataclass
    Returns:
        This function will spawn and remove tape obstacles around the map to make the
        game more enticing.
    """
    random_list = []
    tape_list = world.tape_list
    if len(tape_list) > 0:
        if randint(1, 100) == 4:
            random_tape_index = randint(0, len(tape_list) - 1)
            tape_variable = tape_list[random_tape_index]
            random_list.append(tape_variable)
            world.tape_list = filter_from(world.tape_list, random_list)


def clicking_coordinate(x: int, y: int):
    print('X Coordinate:', str(x))
    print('Y Coordinate:', str(y))


# ----------------------------------------------------------------------------------------#
def user_colliding_platform(world: World):
    """
    This is function is what detects whether the user is hitting the 'ladder' or in the python world, the
    invisible rectangles that are in place where the ladders are. This function utilizes the collision function
    to make the character go up when the user is in contact to the ladder.
    Args:
        world: World dataclass
    Returns:
        This function makes the player go up the ladder.
    """
    global JUMPING_HEIGHT, GRAVITY
    for num, ladder in enumerate(world.ladder_list):
        if colliding(ladder, world.main_character.character_image):
            if (ladder.y - (ladder.height / 2) - 28 < world.main_character.character_image.y < ladder.y +
                    (ladder.height / 2) + 5 and (ladder.x - 30) < world.main_character.character_image.x <
                    (ladder.x + 30)):
                world.main_character.character_image.y -= 5
        elif not colliding(ladder, world.main_character.character_image):
            if not round(world.main_character.character_image.y) >= 494:
                pass
                # world.main_character.character.y += 1


def user_colliding_magnify(world: World):
    """
    This is function detects when the user has touched a Magnifying Glass Power-up. The function will remove a
    magnifying glass from the world dataclass magnifying glass list in order to remove one from the game.
    Once it's been registered in the game that the user touched this power-up, it will increase the size of the
    player making him have an "extra" life.
    Args:
        world: World dataclass
    Returns:
        Will create the player bigger is the power-up is hit.
    """
    destroyed_magnifying_glass = []
    for glass in world.magnifying_glass_list:
        if colliding(glass, world.main_character.character_image):
            world.main_character.character_image.scale = .0275
            destroyed_magnifying_glass.append(glass)
    world.magnifying_glass_list = filter_from(world.magnifying_glass_list, destroyed_magnifying_glass)


def user_colliding_eraser(world: World):
    """
    This is function detects when the user has touched an eraser Power-up. The function will remove a
    eraser from the world dataclass eraser list in order to remove one from the game.
    Once it's been registered in the game that the user touched this power-up, it will decrease the size of the
    player making him smaller and harder to hit
    Args:
        world: World dataclass
    Returns:
        Will create the player to be smaller if the power-up is hit.
    """
    destroyed_eraser_list = []
    for eraser in world.eraser_list:
        if colliding(eraser, world.main_character.character_image):
            world.main_character.character_image.scale = .015
            destroyed_eraser_list.append(eraser)
    world.eraser_list = filter_from(world.eraser_list, destroyed_eraser_list)


def user_colliding_tape_obstacle(world: World):
    """
    This is function detects when the user has touched a tape obstacle. The function will remove a
    tape obstacle from the world dataclass tape list in order to remove one from the game.
    Once it's been registered in the game that the user touched this obstacle, the game will end if the user
     hasn't gotten a magnifying glass power-up.
    Args:
        world: World dataclass
    Returns:
        This function will end the game depending on the status of the player.
    """
    destroyed_tape = []
    for tape in world.tape_list:
        if colliding(tape, world.main_character.character_image):
            game_over()


def user_colliding_crown(world: World):
    """
    This is function is checking if the user collides with the crown which will end with the user
    'winning' the game
    Args:
        world: The World Dataclass
    Returns:
        This function will display the winning screen if the user hits the crown
    """
    if colliding(world.crown, world.main_character.character_image):
        winning_game_over()


def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    """
    This is function is a helper function for the 'colliding' functions. This is what removes power-ups or tape
    obstacles from the world lists.
    Args:
        old_list: This is the old list that the world had in a certain field.
        elements_to_not_keep: This list indicates what will be removed from the world field list
    Returns:
        This function creates a new list with the updated number of power-ups and tape obstacles.
    """
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values


# ----------------------------------------------------------------------------------------#

def game_over():
    """
    This function pushes the Game Over screen

    Returns:
        Will display the Game Over Screen with the option to end the game
    """
    push_scene('game-over')


def winning_game_over():
    """
    This function pushes the winner screen

    Returns:
        Will display the winner Screen with the option to end the game
    """
    push_scene('winning-screen')


# ----------------------------------------------------------------------------------------#

when('starting: world', create_world)
when('clicking: world', handle_world_pause_button)

when('starting: pause', create_pause_screen)
when('clicking: pause', handle_pause_screen_buttons)

when('starting: game-over', create_game_over_screen)
when('clicking: game-over', handle_game_over_screen_buttons)

when('starting: winning-screen', create_winner_screen)
when('clicking: winning-screen', handle_winner_screen_buttons)

when('typing: world', press_moving_keys)

when('updating: world', make_powerup_magnifying_glass)
when('updating: world', make_powerup_eraser)
when('updating: world', make_tape_obstacle)
when('updating: world', teleport_obstacles)
when('updating: world', user_colliding_magnify)
when('updating: world', user_colliding_eraser)
when('updating: world', user_colliding_tape_obstacle)
when('updating: world', user_colliding_platform)
when('updating: world', user_colliding_crown)

when('done typing: world', release_moving_keys)
when('updating: world', handle_movement)
when('updating: world', border_restraining)

when('clicking: world', clicking_coordinate)
when('clicking: pause', handle_pause_screen_buttons)

start()
