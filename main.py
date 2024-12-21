from pgzero.actor import Actor
from pgzero.builtins import *
import pgzero.screen
from var import *
import copy, pgzrun, os, sys
screen: pgzero.screen.Screen

WIDTH = 1036
HEIGHT = 740
TITLE = "LogicCraft"
FPS = 30

menu_fon = Actor('menu_fon')
play = Actor('play', (WIDTH/2, HEIGHT/2+100))
text = Actor('text', (WIDTH/2, HEIGHT/2-150))
home = Actor('home', (WIDTH/2-WIDTH/4, HEIGHT/2))
next = Actor('next', (WIDTH/2+WIDTH/4, HEIGHT/2))
victory = Actor('victory')
end = Actor('end')
exit_button = Actor('exit', (WIDTH/2+WIDTH/4, HEIGHT/2+HEIGHT/6))
info = Actor('info', (WIDTH/2-WIDTH/4, HEIGHT/2+HEIGHT/6))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

game_objects = []
list_of_map = [level_1_map, level_2_map, level_3_map, level_4_map, level_5_map, level_6_map]
selected_object = None
mode = 'menu'
level = 0
map = level_1_map
last_move = None
font = resource_path('fonts/minecraft.ttf')

def map_draw():
    if level != 0:
        for i in range(len(map)):
            for j in range(len(map[0])):
                value = map[i][j]
                x = j * 74
                y = i * 74
                if value == 1:
                    new_block = Actor(resource_path('images/блок.jpg'))
                elif value == 2:
                    new_block = Actor(resource_path('images/рычаг.jpg'))
                elif value == 3:
                    new_block = Actor(resource_path('images/redstone_lamp.png'))
                elif value == 4:
                    new_block = Actor(resource_path('images/фон_квадрат.jpg'))
                elif value == 5:
                    new_block = Actor(resource_path('images/белый_квадрат.jpg'))
                elif value == 6:
                    new_block = Actor(resource_path('images/redstone_lamp_on.png'))
                elif value == 8:
                    new_block = Actor(resource_path('images/thirth_redstone_line_to_right.jpg'))
                elif value == 13:
                    new_block = Actor(resource_path('images/redstone_torch_on_wall_of_block.jpg'))
                elif value == 14:
                    new_block = Actor(resource_path('images/redstone_torch_on_block.jpg'))
                elif value == 16:
                    new_block = Actor(resource_path('images/richag_up.jpg'))
                elif value == 17:
                    new_block = Actor(resource_path('images/richag_down.jpg'))
                new_block.left = x
                new_block.top = y
                new_block.index = (i, j)
                new_block.draw()
                game_objects.append(new_block)

# def scan_block(i, j):
#     global map
#     for block in game_objects:
#         if block.index == (i, j):
#             map[i][j] = 6

def update():
    global mode, time_var
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 2:
                if level == 1:
                    if j + 1 < len(map[0]) and map[i][j + 1] == 1 and j + 2 < len(map[0]) and map[i][j + 2] == 3:  # Проверка на наличие блока и лампы справа
                        # scan_block(i, j+2)
                        mode = 'victory'
                if level == 2:
                    if j + 1 < len(map[0]) and map[i][j + 1] == 1 and j + 2 < len(map[0]) and map[i][j + 2] == 13 and j + 3 < len(map[0]) and map[i][j + 3] == 3:  # Проверка на наличие блока и лампы справа
                        mode = 'victory'

            if level == 3:
                if map[i][j] == 16:
                    if i + 1 < len(map) and map[i+1][j] == 1 and i + 2 < len(map) and map[i+2][j] == 17 and j + 1 < len(map[i]) and map[i + 1][j + 1] == 3:
                        mode = 'victory'
            
            if level == 4:
                if map[i][j] == 2:
                    if i + 2 < len(map) and map[i+2][j] == 2 and j + 1 < len(map[0]) and map[i][j + 1] == 14 and (i + 1 < len(map) and j + 1 < len(map[0])) and map[i+1][j+1] == 8 and (j + 1 < len(map[0]) and i + 2 < len(map)) and map[i+2][j + 1] == 14 and (i + 1 < len(map) and j + 2 < len(map[0])) and map[i+1][j+2] == 13 and (i + 1 < len(map) and j + 3 < len(map[0])) and map[i+1][j+3] == 3:
                        mode = 'victory'

            if level == 5:
                if map[i][j] == 16:
                    if i + 1 < len(map) and map[i+1][j] == 1 and i + 2 < len(map) and map[i+2][j] == 17 and j + 1 < len(map[i]) and map[i + 1][j + 1] == 13 and (i + 1 < len(map) and j + 2 < len(map[i])) and map[i+1][j+2] == 3:
                        mode = 'victory'

            if level == 6:
                if map[i][j] == 2:
                    if i + 2 < len(map) and map[i+2][j] == 2 and j + 1 < len(map[0]) and map[i][j + 1] == 14 and (i + 1 < len(map) and j + 1 < len(map[0])) and map[i+1][j+1] == 8 and (j + 1 < len(map[0]) and i + 2 < len(map)) and map[i+2][j + 1] == 14 and (i + 1 < len(map) and j + 3 < len(map[0])) and map[i+1][j+2] == 3:
                        mode = 'victory-end'
        


def on_mouse_down(button, pos):
    global game_objects, selected_object, mode, last_move, map, level, list_of_map
    if button == mouse.LEFT and mode == 'game':
        for obj in game_objects:
            if obj.collidepoint(pos):
                selected_object = obj.index
                break
    
    # elif button == mouse.RIGHT and mode == 'game':
    #     for obj in game_objects:
    #         if obj.collidepoint(pos):
    #             obj.angle += 90
    #             break

    if button == mouse.LEFT and (mode == 'victory' or mode == 'victory-end' or mode == 'info') and home.collidepoint(pos):
        mode = 'menu'
        level = 0
        selected_object = None
        last_move = None
    
    if button == mouse.LEFT and mode == 'victory' and next.collidepoint(pos):
        mode = 'game'
        map = copy.deepcopy(list_of_map[(level-1)+1])
        level += 1
        map_draw()
        selected_object = None
        last_move = None

    if button == mouse.LEFT and mode == 'menu' and play.collidepoint(pos):
        mode = 'game'
        level = 1
        map = copy.deepcopy(list_of_map[(level-1)])
        game_objects.clear()
        map_draw()

    if button == mouse.LEFT and mode == 'menu' and exit_button.collidepoint(pos):
        exit()
    
    if button == mouse.LEFT and mode == 'menu' and info.collidepoint(pos):
        mode = 'info'

def move_object(di, dj):
    global selected_object, last_move
    if selected_object != None and mode == 'game':
        i, j = selected_object
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < len(map) and 0 <= new_j < len(map[0]):
            # if map[new_i][new_j] == 5:  недоделанное изменение белого квадрата
            #     map[new_i][new_j] = 4
            map[i][j], map[new_i][new_j] = map[new_i][new_j], map[i][j] 
            selected_object = (new_i, new_j)
            last_move = (di, dj)
            map_draw()

def on_key_down(key):
    global selected_object, last_move, map, mode, level, time_var
    if selected_object != None and mode == 'game':
        if key == keys.LEFT:
            move_object(0, -1)
        elif key == keys.RIGHT:
            move_object(0, 1)
        elif key == keys.UP:
            move_object(-1, 0)
        elif key == keys.DOWN:
            move_object(1, 0)
    
    if (mode == 'info' or mode == 'victory' or mode == 'victory-end' or mode == 'game') and key == keys.ESCAPE:
        mode = 'menu'
        level = 0
        selected_object = None
        last_move = None

    if mode == 'victory' and key == keys.SPACE:
        mode = 'game'
        map = copy.deepcopy(list_of_map[(level-1)+1])
        level += 1
        map_draw()
        selected_object = None
        last_move = None

def draw():
    if mode == 'menu':
        menu_fon.draw()
        play.draw()
        text.pos = (WIDTH/2, HEIGHT/2-150)
        text.draw()
        exit_button.draw()
        info.draw()

    elif mode == 'game':
        map_draw()
        if level == 1:
            text_level = 'Input Gate'
        elif level == 2:
            text_level = 'NOT Gate'
        elif level == 3:
            text_level = 'OR Gate'
        elif level == 4:
            text_level = 'AND Gate'
        elif level == 5:
            text_level = 'NOR Gate'
        elif level == 6:
            text_level = 'NAND Gate'
        screen.draw.text(text_level, center=(WIDTH/2, HEIGHT/8), fontsize=40, color='black', fontname=font, align='center')
            
    elif mode == 'victory':
        home.pos = (WIDTH/2-WIDTH/4, HEIGHT/2)
        home.draw()
        next.draw()
        screen.draw.text(f'Level {level} completed!', center=(WIDTH/2, HEIGHT/8), fontsize=40, color='black', fontname=font, align='center')

    elif mode == 'victory-end':
        home.pos = (WIDTH/2, HEIGHT/2)
        home.draw()
        screen.draw.text(f'Level {level} completed!', center=(WIDTH/2, HEIGHT/8), fontsize=40, color='black', fontname=font, align='center')
    
    elif mode == 'info':
        menu_fon.draw()
        text.pos = (WIDTH/2, HEIGHT/8)
        text.draw()
        home.pos = (WIDTH/2, HEIGHT/4+460)
        home.draw()

        screen.draw.text('Left Mouse Button Click - block selection', center=(WIDTH/2, HEIGHT/4), fontsize=30, color='black', fontname=font, align='center')
        screen.draw.text('Left Arrow - move left', center=(WIDTH/2, HEIGHT/4+40), fontsize=30, color='black', fontname=font, align='center')
        screen.draw.text('Right Arrow - move right', center=(WIDTH/2, HEIGHT/4+80), fontsize=30, color='black', fontname=font, align='center')
        screen.draw.text('Up Arrow - move up', center=(WIDTH/2, HEIGHT/4+120), fontsize=30, color='black', fontname=font, align='center')
        screen.draw.text('Down Arrow - move down', center=(WIDTH/2, HEIGHT/4+160), fontsize=30, color='black', fontname=font, align='center')

        screen.draw.text('ESC key or HOME button, to leave to the menu', center=(WIDTH/2, HEIGHT/4+210), fontsize=30, color='black', fontname=font, align='center')
        screen.draw.text('SPACE key or NEXT button, to go to the next level', center=(WIDTH/2, HEIGHT/4+250), fontsize=30, color='black', fontname=font, align='center')

        screen.draw.text('The textures of the PLAY, INFO, EXIT and NEXT buttons are taken from icon8.com', center=(WIDTH/2, HEIGHT/4+290), fontsize=15, color='black', fontname=font, align='center')
        screen.draw.text('The texture of the HOME button are taken from flaticon.com', center=(WIDTH/2, HEIGHT/4+310), fontsize=15, color='black', fontname=font, align='center')
        screen.draw.text('The texture of the blocks are taken from Minecraft', center=(WIDTH/2, HEIGHT/4+330), fontsize=15, color='black', fontname=font, align='center')
        screen.draw.text('The Minecraft font are taken from fonts-online.ru', center=(WIDTH/2, HEIGHT/4+350), fontsize=15, color='black', fontname=font, align='center')

pgzrun.go()