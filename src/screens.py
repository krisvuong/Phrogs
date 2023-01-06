import pygame
import random
import os
from classes import *
from classes import Game
import copy

# INITIALIZE GAME STUFF ————————————————————————————————————————————————————————————
pygame.mixer.init()
music_directory = "src/assets/music/"
font_file = "src/assets/fonts/04B30.TTF"
# Create main game
a = Player()
b = Player()
game = Game(a, b)

# Read creatures text file
cname = "src/stats/creatures_stats.txt"
iname = "src/stats/items_stats.txt"
game.read_creatures(cname)
game.read_items(iname)
pygame.init()


def main_menu():
    pygame.mixer.music.load(music_directory + 'main_menu.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()  # Set pygame clock
    (width, height) = (1280, 720)  # Width and height of windopw
    screen = pygame.display.set_mode((width, height))  # or FULLSCREEN
    pygame.display.set_caption('PHROGS')  # Set window title
    background_colour = (255, 255, 0)
    running = True  # Main screen loop
    screen_x, screen_y = screen.get_size()  # Get size of window

    # LOAD FILES (sprites, fonts...) ----------------------------------------------------------------------------------

    # Load main menu background image
    menu = pygame.image.load('src/assets/main_menu.jpg!d')  # Background image
    pygame.transform.scale(menu, (1920, 1080))  # Scale background image
    click_sound = pygame.mixer.Sound(music_directory + 'select.mp3')

    # Load game title image
    cwd = os.getcwd()
    title = pygame.image.load("src/assets/title2.png")  # Load random file as an image
    title_w = title.get_width() * 1.5  # Use to scale image later
    title_h = title.get_height() * 1.5

    # Load Play Game image
    play_image = pygame.image.load("src/assets/Play_Game.png")  # Load random file as an image
    play_w = play_image.get_width() * 0.8  # Use to scale image later
    play_h = play_image.get_height() * 0.8

    # MAIN SCREEN LOOP ------------------------------------------------------------------------------------------------
    x = -4  # Used as counter for animation (x value of function)
    while running:

        # Set up display
        click = False
        screen.fill(background_colour)  # Fill background colour

        # Get current position of mouse
        mx, my = pygame.mouse.get_pos()

        # Create "play game" button
        width_play_game = 900
        height_play_game = 200
        if x <= 7:
            button_play = pygame.Rect((screen_x / 2) - (width_play_game / 2), screen_y - (350 / (1 + (5 ** - x))),
                                      width_play_game, height_play_game)
        else:
            button_play = pygame.Rect((screen_x / 2) - (width_play_game / 2), screen_y - (350 / (1 + (5 ** - 7))),
                                      width_play_game, height_play_game)

        # Draw background image to screen
        menu = pygame.transform.scale(menu, (screen_x, screen_y))
        screen.blit(menu, (0, 0))

        # Draw game title logo to screen
        title = pygame.transform.scale(title, (title_w, title_h))
        x += 0.05
        if x <= 7:  # Animate title logo into screen
            screen.blit(title, ((screen_x / 2) - (title_w / 2), -150 + (350 / (1 + (5 ** - x)))))
        else:
            screen.blit(title, ((screen_x / 2) - (title_w / 2), -150 + (350 / (1 + (5 ** - 7)))))

        # Draw button to screen
        pygame.draw.rect(screen, (255, 189, 0), button_play)

        # Draw "Play Game" image to screen
        play_image = pygame.transform.scale(play_image, (play_w, play_h))
        screen.blit(play_image, ((screen_x / 2) - (play_w / 2), button_play.y + (height_play_game / 2) - (play_h / 2)))

        # Look at all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If press quit
                running = False
            if event.type == pygame.KEYDOWN:  # If press key
                if event.key == pygame.K_ESCAPE:  # If key is escape
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse click
                if event.button == 1:  # If left click
                    click = True
                    pygame.mixer.Sound.play(click_sound)

        # If mouse clicks on "play game" button
        if button_play.collidepoint((mx, my)):
            pygame.draw.rect(screen, (220, 150, 0), button_play)  # Darken button while hovering
            screen.blit(play_image,
                        ((screen_x / 2) - (play_w / 2), button_play.y + (height_play_game / 2) - (play_h / 2)))
            if click:
                fade_out(screen, screen_x, screen_y)
                shop_screen()

        pygame.display.update()
        clock.tick(60)


# Picks a random file from a given directory
def random_file(directory):
    random_file = random.choice(os.listdir(directory))  # Get random file from "Food" folder
    pic = pygame.image.load(directory + "/" + random_file)  # Load random file as an image

    return pic


# Fades passed screen to black
def fade_out(screen, x, y):
    fade = pygame.Surface((x, y))
    fade.fill((0, 0, 0))
    for i in range(0, 100):
        fade.set_alpha(i)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)


# Doesn't work right now but should fade from black to clear
def fade_in(screen, count):
    fade = pygame.Surface((1280, 720))
    fade.fill((0, 0, 0))
    fade.set_alpha(count)
    screen.blit(fade, (0, 0))
    pygame.time.delay(10)


def shop_screen():
    pygame.mixer.music.load(music_directory + 'item_shop.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    (width, height) = (1280, 720)
    screen = pygame.display.set_mode((width, height))  # or FULLSCREEN
    pygame.display.set_caption('PHROGS')
    background_colour = (0, 255, 255)
    screen_x, screen_y = screen.get_size()

    # Load shop background image
    sprites_directory = "src/assets/"  # Get current working directory
    bg = pygame.image.load(sprites_directory + 'shop.jpg')  # Background image
    pygame.transform.scale(bg, (screen_x, screen_y))  # Scale background image

    # Load health and fist image
    health_img = pygame.image.load(sprites_directory + "health.png")
    health_img = pygame.transform.scale(health_img, (50, 50))
    attack_img = pygame.image.load(sprites_directory + "attack.png")
    attack_img = pygame.transform.scale(attack_img, (50, 50))

    # Load roll, sell, end turn labels
    roll_img = pygame.image.load(sprites_directory + "roll.png")
    sell_img = pygame.image.load(sprites_directory + "sell.png")
    end_turn_img = pygame.image.load(sprites_directory + "end_turn.png")

    # Transform roll, sell, end turn labels
    roll_img = pygame.transform.scale(roll_img, (200, 51))
    sell_img = pygame.transform.scale(sell_img, (198, 51))
    end_turn_img = pygame.transform.scale(end_turn_img, (418, 51))

    # Load top icons
    coins_img = pygame.image.load(sprites_directory + "coin.png")
    coins_img = pygame.transform.scale(coins_img, (50, 50))

    turn_img = pygame.image.load(sprites_directory + "turn.png")
    turn_img = pygame.transform.scale(turn_img, (50, 50))

    # Get creature directory
    creature_directory = "src/assets/creatures/"  # Get current working directory

    # Get food directory
    food_directory = "src/assets/food/"  # Get current working directory

    # Create "roll" button
    width = 250
    height = 100
    button_roll = pygame.Rect(20, screen_y - 20 - height, width, height)

    # Create "end turn" button
    width = 470
    height = 100
    button_end_turn = pygame.Rect(screen_x - 20 - width - 5, screen_y - 20 - height, width, height)

    # Create "sell" button
    width = 250
    height = 100
    button_sell = pygame.Rect((screen_x / 2) - (width / 2) - 220, screen_y - 20 - height, width, height)

    players = [a, b]  # List to repeat item shop for both players

    for k in range(2):

        running = True

        scale = 1.4
        frame = pygame.image.load(sprites_directory + str(k + 1) + "_frame.png")
        frame_w = frame.get_width() * scale
        frame_h = frame.get_height() * scale
        frame = pygame.transform.scale(frame, (frame_w, frame_h))

        # Load creature and item objects in shop
        # CHANGE LATER TO FIX FOR TWO PLAYERS
        game.load_shop(players[k], True)
        click_sound = pygame.mixer.Sound(music_directory + 'select.mp3')
        sell_sound = pygame.mixer.Sound(music_directory + 'sell.mp3')
        roll_sound = pygame.mixer.Sound(music_directory + 'crank.mp3')
        place_sound = pygame.mixer.Sound(music_directory + 'place.mp3')
        food_sound = pygame.mixer.Sound(music_directory + 'munch.mp3')

        # Handle if player clicks a creature or item
        hold_click = False
        food_click = False
        creature_choice = 0
        food_choice = 0
        swap_pos = []
        sell_click = False

        while running:
            creature_rects = []
            food_rects = []
            frame_rects = []
            click = False
            screen.fill(background_colour)  # Fill background colour
            # Draw bg image to screen
            bg = pygame.transform.scale(bg, (screen_x, screen_y))
            screen.blit(bg, (0, 0))
            for i in range(-2, 3):
                screen.blit(frame, ((screen_x / 2) - (frame_w / 2) + (frame_w * 1.2 * i), 100))

            # Blit creatures and frames to shop
            for i in range(len(game.creature_shop)):
                img_name = str(game.creature_shop[i].num) + ".png"
                creature_pic = pygame.image.load(creature_directory + img_name)
                creature_pic = pygame.transform.scale(creature_pic, (150, 150))
                screen.blit(creature_pic, (100 + (150 * i) + 20, (screen_y / 5) * 2.75))
                # Make rectangles from pictures
                temp_rect = creature_pic.get_rect()
                temp_rect.left = 100 + (150 * i) + 20
                temp_rect.top = (screen_y / 5) * 2.75
                creature_rects.append(temp_rect)

                screen.blit(attack_img, ((100 + (150 * i) + 45), ((screen_y / 5) * 2.75 + creature_pic.get_height())))
                screen.blit(health_img, ((100 + (150 * i) + 105), ((screen_y / 5) * 2.75 + creature_pic.get_height())))

                font = pygame.font.Font(font_file, 20)
                icon_font = pygame.font.Font(font_file, 30)

                damage = str(game.creature_shop[i].damage)
                health = str(game.creature_shop[i].health)

                dmg_text = font.render(damage, True, (220, 189, 0))
                health_text = font.render(health, True, (220, 189, 0))

                dmg_text_rect = dmg_text.get_rect()
                dmg_w = dmg_text.get_width()

                health_text_rect = health_text.get_rect()
                health_w = health_text.get_width()

                dmg_text_rect.left = 100 + (150 * i) + 60
                health_text_rect.left = 100 + (150 * i) + 120

                dmg_text_rect.top = (screen_y / 5) * 2.75 + creature_pic.get_height() + 15
                health_text_rect.top = (screen_y / 5) * 2.75 + creature_pic.get_height() + 15

                screen.blit(dmg_text, dmg_text_rect)
                screen.blit(health_text, health_text_rect)

            # Create rectangles from frames
            for i in range(-2, 3):
                temp_rect = frame.get_rect()
                temp_rect.left = (screen_x / 2) - (frame_w / 2) + (frame_w * 1.2 * i)
                temp_rect.top = 100
                frame_rects.append(temp_rect)

            # Blit food pictures to shop
            for i in range(len(game.item_shop)):
                img_name = str("food_" + game.item_shop[i].name + ".png")
                food_pic = pygame.image.load(food_directory + img_name)

                food_w = food_pic.get_width()
                food_h = food_pic.get_height()
                scale = 100 / food_h
                food_pic = pygame.transform.scale(food_pic, (food_w * scale, food_h * scale))
                screen.blit(food_pic, (200 + (screen_x / 2) + (150 * i) + 50, (screen_y / 5) * 3 + 50))

            # Create rectangles from food items
            for i in range(len(game.item_shop)):
                img_name = str("food_" + game.item_shop[i].name + ".png")
                food_pic = pygame.image.load(food_directory + img_name)
                temp_rect = food_pic.get_rect()

                temp_rect.left = 200 + (screen_x / 2) + (150 * i) + 50
                temp_rect.top = (screen_y / 5) * 3 + 50

                food_rects.append(temp_rect)

            # Blit creature pictures to top frames
            for i in range(len(players[k].team)):
                if players[k].team[i] != 0:
                    img_name = str(creature_directory + str(players[k].team[i].num) + ".png")
                    img = pygame.image.load(img_name)
                    img = pygame.transform.scale(img, (125, 125))
                    screen.blit(img, (((screen_x / 2) - (125 / 2) + (frame_w * 1.2 * (i - 2))), 125))

            # Draw health and damage under each creature
            for i in range(len(players[k].team)):
                if players[k].team[i] != 0:
                    screen.blit(attack_img, ((screen_x / 2) - (50 / 2) + (frame_w * 1.2 * (i - 2)) - 30, 285))
                    screen.blit(health_img, ((screen_x / 2) - (50 / 2) + (frame_w * 1.2 * (i - 2)) + 30, 285))

                    font = pygame.font.Font(font_file, 20)

                    damage = str(players[k].team[i].damage)
                    health = str(players[k].team[i].health)

                    dmg_text = font.render(damage, True, (220, 189, 0))
                    health_text = font.render(health, True, (220, 189, 0))

                    dmg_text_rect = dmg_text.get_rect()
                    dmg_w = dmg_text.get_width()

                    health_text_rect = health_text.get_rect()
                    health_w = health_text.get_width()

                    dmg_text_rect.left = (screen_x / 2) - (dmg_w / 2) + (frame_w * 1.2 * (i - 2)) - 30
                    health_text_rect.left = (screen_x / 2) - (health_w / 2) + (frame_w * 1.2 * (i - 2)) + 30

                    dmg_text_rect.top = 300
                    health_text_rect.top = 300

                    screen.blit(dmg_text, dmg_text_rect)
                    screen.blit(health_text, health_text_rect)

            # Blit top pictures to screen
            screen.blit(health_img, (25, 15))
            temp_text = icon_font.render(str(players[k].lives), True, (0, 0, 0))
            temp_rect = temp_text.get_rect()
            temp_rect.left = 25 + 60
            temp_rect.top = 25
            screen.blit(temp_text, temp_rect)

            screen.blit(coins_img, (150, 15))
            temp_text = icon_font.render(str(players[k].coins), True, (0, 0, 0))
            temp_rect = temp_text.get_rect()
            temp_rect.left = 150 + 60
            temp_rect.top = 25
            screen.blit(temp_text, temp_rect)

            screen.blit(turn_img, (screen_x - 100, 15))
            temp_text = icon_font.render(str(game.turns), True, (0, 0, 0))
            temp_rect = temp_text.get_rect()
            temp_rect.left = screen_x - 50
            temp_rect.top = 25
            screen.blit(temp_text, temp_rect)

            """

            dmg_text = font.render(damage, True, (220, 189, 0))
            health_text = font.render(health, True, (220, 189, 0))

            dmg_text_rect = dmg_text.get_rect()
            health_text_rect = health_text.get_rect()

            dmg_text_rect.left = 460 - (115 * (len(a_creatures) - count)) - 20 + 175
            health_text_rect.left = 460 - (115 * (len(a_creatures) - count)) + 20 + 175

            dmg_text_rect.top = 665
            health_text_rect.top = 665

            screen.blit(dmg_text, dmg_text_rect)
            screen.blit(health_text, health_text_rect)
            """
            # Get position of mouse
            mx, my = pygame.mouse.get_pos()

            # Look at all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If press quit
                    running = False
                if event.type == pygame.KEYDOWN:  # If press key
                    if event.key == pygame.K_ESCAPE:  # If key is escape
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # If click
                    if event.button == 1:  # If left click
                        click = True
                        sell_click = False

            # If mouse clicks on "roll" button
            if button_roll.collidepoint((mx, my)):
                if click and players[k].coins >= 1:
                    pygame.mixer.Sound.play(roll_sound)
                    # CHANGE LATER TO FIX FOR TWO PLAYERS
                    game.load_shop(players[k], False)  # Reloads shop
                    print(players[k].coins)

            # If mouse consecutively clicks on two creatures (switch position)
            if not hold_click and not food_click:
                for i in range(len(frame_rects)):
                    if frame_rects[i].collidepoint((mx, my)) and click:
                        pygame.mixer.Sound.play(click_sound)
                        swap_pos.append(i)
                if len(swap_pos) == 2:
                    players[k].team[swap_pos[0]], players[k].team[swap_pos[1]] = players[k].team[swap_pos[1]], \
                                                                                 players[k].team[swap_pos[0]]
                    swap_pos = []
                    sell_click = False

            # If click creature and click sell
            if not hold_click and not food_click:
                for i in range(len(frame_rects)):
                    if frame_rects[i].collidepoint((mx, my)) and click:
                        pygame.mixer.Sound.play(click_sound)
                        creature_choice = i
                        sell_click = True
                if players[k].team[creature_choice] != 0 and button_sell.collidepoint((mx, my)) and click:
                    pygame.mixer.Sound.play(sell_sound)
                    players[k].sell_creature(creature_choice)
                    sell_click = False
                    swap_pos = []

            # If mouse clicks on a creature and buys
            for i in range(len(creature_rects)):
                if creature_rects[i].collidepoint((mx, my)) and click:
                    pygame.mixer.Sound.play(click_sound)
                    hold_click = True
                    food_click = False
                    creature_choice = i
            for i in range(5):
                if frame_rects[i].collidepoint((mx, my)) and hold_click and click:
                    pygame.mixer.Sound.play(place_sound)
                    hold_click = False
                    swap_pos = []
                    print(players[k].coins)
                    if players[k].coins >= 3:  # Remove bought creature from shop
                        players[k].buy_creature(game.creature_shop[creature_choice], i)
                        game.creature_shop.pop(creature_choice)
            # creature_choice = 0

            # If mouse clicks on a food item
            for i in range(len(food_rects)):
                if food_rects[i].collidepoint((mx, my)) and click:
                    pygame.mixer.Sound.play(click_sound)
                    food_click = True
                    hold_click = False
                    food_choice = i
            for i in range(5):
                if frame_rects[i].collidepoint((mx, my)) and food_click and click:
                    food_click = False
                    swap_pos = []
                    if players[k].team[i] != 0 and players[k].coins >= 3:
                        pygame.mixer.Sound.play(food_sound)
                        players[k].team[i].health = players[k].team[i].change_health(game.item_shop[food_choice].health)
                        players[k].team[i].damage = players[k].team[i].change_damage(game.item_shop[food_choice].damage)
                        game.item_shop.pop(food_choice)
                        players[k].coins -= 3

            # If mouse clicks on "end turn" button
            if button_end_turn.collidepoint((mx, my)) and click:
                pygame.mixer.Sound.play(click_sound)
                fade_out(screen, screen_x, screen_y)
                if k == 1:

                    queue_tup = game.end_turn(players[0].team, players[1].team)
                    player_1 = queue_tup[0]  # Queues of player teams
                    player_2 = queue_tup[1]
                    running = False

                else:
                    running = False

            # Draw button to screen
            pygame.draw.rect(screen, (255, 189, 0), button_roll)
            screen.blit(roll_img, (20 + 125 - 100, screen_y - 20 - height + 20))

            pygame.draw.rect(screen, (255, 189, 0), button_end_turn)
            screen.blit(end_turn_img, (screen_x - 20 - width - 200, screen_y - 20 - height + 20))

            if sell_click:
                pygame.draw.rect(screen, (255, 189, 0), button_sell)
                screen.blit(sell_img, ((screen_x / 2) - (width / 2) - 193, screen_y - 20 - height + 20))

                if button_sell.collidepoint((mx, my)):
                    pygame.draw.rect(screen, (220, 150, 0), button_sell)
                    screen.blit(sell_img, ((screen_x / 2) - (width / 2) - 193, screen_y - 20 - height + 20))

            # Make buttons darken when hovering

            if button_roll.collidepoint((mx, my)):
                pygame.draw.rect(screen, (220, 150, 0), button_roll)
                screen.blit(roll_img, (20 + 125 - 100, screen_y - 20 - height + 20))

            if button_end_turn.collidepoint((mx, my)):
                pygame.draw.rect(screen, (220, 150, 0), button_end_turn)
                screen.blit(end_turn_img, (screen_x - 20 - width - 200, screen_y - 20 - height + 20))

            pygame.display.update()
            clock.tick(60)

    battle_screen(player_1, player_2)


def battle_screen(player_1, player_2):
    pygame.mixer.music.load(music_directory + 'battle.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()  # Set pygame clock
    (width, height) = (1280, 720)  # Width and height of window
    screen = pygame.display.set_mode((width, height))  # or FULLSCREEN
    pygame.display.set_caption('PHROGS')  # Set window caption
    background_colour = (0, 255, 0)  # Set background colour of display
    running = True
    screen_x, screen_y = screen.get_size()  # Dimensions of pygame window
    game.turns += 1

    # Used to delay screen updates
    timer = 0

    # LOAD FILES (sprites, fonts...) ----------------------------------------------------------------------------------

    # Load main menu background image
    sprites_directory = "src/assets/"  # Get current working directory
    bg = pygame.image.load(sprites_directory + 'battle.jpg')  # Background image

    creatures_directory = "src/assets/creatures/"  # Get current working directory

    # Load sounds
    hurt_sound = pygame.mixer.Sound(music_directory + 'ow.mp3')

    # Load health and attack images
    health_img = pygame.image.load(sprites_directory + "health.png")
    health_img = pygame.transform.scale(health_img, (40, 40))
    attack_img = pygame.image.load(sprites_directory + "attack.png")
    attack_img = pygame.transform.scale(attack_img, (40, 40))

    # MAIN SCREEN LOOP ------------------------------------------------------------------------------------------------
    while running:
        click = False
        a_creatures = []
        b_creatures = []

        # Update player queues
        for i in range(len(player_1.items)):
            try:
                a_creatures.append(
                    pygame.transform.scale(pygame.image.load(creatures_directory + str(player_1.look(i).num) + ".png"),
                                           (140, 140)))
            except:
                pass

        for i in range(len(player_2.items)):
            try:
                b_creatures.append(
                    pygame.transform.scale(pygame.image.load(creatures_directory + str(player_2.look(i).num) + ".png"),
                                           (140, 140)))
            except:
                pass

        # Battle stuff (logic)

        # Creatures attack each other
        print(player_1.look(0).name, player_1.look(0).damage, player_1.look(0).health)
        print(player_2.look(0).name, player_2.look(0).damage, player_2.look(0).health)
        print()

        # Set up display
        screen.fill(background_colour)

        # Get position of mouse
        mx, my = pygame.mouse.get_pos()

        # Draw bg image to screen
        bg = pygame.transform.scale(bg, (screen_x, screen_y))
        screen.blit(bg, (0, 0))

        # Load font
        font = pygame.font.Font(font_file, 20)

        # Draw team A creatures to screen
        for i in range(len(a_creatures)):
            # Draw team A creatures
            screen.blit(a_creatures[i], (460 - (115 * i), height - 200))
            # Blit attack and health images under each creature
            screen.blit(attack_img, (460 - (115 * i) - 20 + 50, 655))
            screen.blit(health_img, (460 - (115 * i) + 20 + 50, 655))

        # Draw team B creatures to screen
        for i in range(len(b_creatures)):
            screen.blit(b_creatures[i], (640 + (115 * i), height - 200))
            # Blit attack and health images under each creature
            screen.blit(attack_img, (640 + (115 * i) - 20 + 50, 655))
            screen.blit(health_img, (640 + (115 * i) + 20 + 50, 655))

        # Write team A stats under each creature
        count = -1
        for i in range(5):
            if a.team[i] != 0:
                count += 1

                # Draw attack and health stats on heart and fist images
                if count < len(player_1.items):
                    damage = str(player_1.look(len(player_1.items) - count - 1).damage)
                    health = str(player_1.look(len(player_1.items) - count - 1).health)

                    dmg_text = font.render(damage, True, (220, 189, 0))
                    health_text = font.render(health, True, (220, 189, 0))

                    dmg_text_rect = dmg_text.get_rect()
                    health_text_rect = health_text.get_rect()

                    dmg_text_rect.left = 460 - (115 * (len(a_creatures) - count)) - 20 + 175
                    health_text_rect.left = 460 - (115 * (len(a_creatures) - count)) + 20 + 175

                    dmg_text_rect.top = 665
                    health_text_rect.top = 665

                    screen.blit(dmg_text, dmg_text_rect)
                    screen.blit(health_text, health_text_rect)

        # Write team B stats under each creature
        count = -1
        for i in range(5):
            if b.team[i] != 0:
                count += 1

                # Draw attack and health stats on heart and fist images
                if count < len(player_2.items):
                    damage = str(player_2.look(count).damage)
                    health = str(player_2.look(count).health)

                    dmg_text = font.render(damage, True, (220, 189, 0))
                    health_text = font.render(health, True, (220, 189, 0))

                    dmg_text_rect = dmg_text.get_rect()
                    health_text_rect = health_text.get_rect()

                    dmg_text_rect.left = 640 + (115 * count) - 20 + 63
                    health_text_rect.left = 640 + (115 * count) + 20 + 63

                    dmg_text_rect.top = 665
                    health_text_rect.top = 665

                    screen.blit(dmg_text, dmg_text_rect)
                    screen.blit(health_text, health_text_rect)

        # Creatures attack each other
        player_2.look(0).health = player_1.look(0).attack(player_2.look(0))
        player_1.look(0).health = player_2.look(0).attack(player_1.look(0))
        pygame.mixer.Sound.play(hurt_sound)

        print("empty:", player_1.is_empty())
        # Remove fainted creatures (if health <= 0)
        if player_1.look(0).health <= 0:  # If a creature faints, remove it
            player_1.dequeue(0)  # Next creature moves to the front
        if player_2.look(0).health <= 0:
            player_2.dequeue(0)

        a_creatures = []
        b_creatures = []

        # Update player queues
        for i in range(len(player_1.items)):
            try:
                a_creatures.append(
                    pygame.transform.scale(
                        pygame.image.load(creatures_directory + str(player_1.look(i).num) + ".png"),
                        (140, 140)))
            except:
                pass

        for i in range(len(player_2.items)):
            try:
                b_creatures.append(
                    pygame.transform.scale(
                        pygame.image.load(creatures_directory + str(player_2.look(i).num) + ".png"),
                        (140, 140)))
            except:
                pass
        # Look at all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If press quit
                running = False
            if event.type == pygame.KEYDOWN:  # If press key
                if event.key == pygame.K_ESCAPE:  # If key is escape
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # If click
                if event.button == 1:  # If left click
                    click = True

        if player_1.is_empty():
            print("1 is empty")
            game.player_2.wins += 1
            game.player_1.lives -= 1
            running = False

        elif player_2.is_empty():
            print("3 is empty")
            game.player_1.wins += 1
            game.player_2.lives -= 1
            running = False

        pygame.display.update()
        pygame.time.wait(2000)
        clock.tick(60)

    winner = ''
    if a.lives == 0:
        game_over("B")
    elif b.lives == 0:
        game_over("A")
    else:
        game.load_shop(a, True)
        game.load_shop(b, True)
        fade_out(screen, screen_x, screen_y)
        shop_screen()


def game_over(player):
    # pygame.mixer.music.load(music_directory + 'win.mp3')
    # pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()  # Set pygame clock
    (width, height) = (1280, 720)  # Width and height of window
    screen = pygame.display.set_mode((width, height))  # or FULLSCREEN
    pygame.display.set_caption('PHROGS')  # Set window caption
    background_colour = (0, 255, 0)  # Set background colour of display
    running = True
    screen_x, screen_y = screen.get_size()  # Dimensions of pygame window
    click_sound = pygame.mixer.Sound(music_directory + 'select.mp3')

    # Load battle background image
    sprites_directory = "src/assets/"  # Get current working directory
    bg = pygame.image.load(sprites_directory + 'battle.jpg')  # Background image
    bg = pygame.transform.scale(bg, (screen_x, screen_y))  # Scale background image

    while running:

        # Set up display
        screen.fill(background_colour)
        pygame.transform.scale(bg, (screen_x, screen_y))  # Scale background image

        # Get position of mouse
        mx, my = pygame.mouse.get_pos()

        # Draw bg image to screen
        screen.blit(bg, (0, 0))

        winner_font = pygame.font.Font(font_file, 60)
        winner = "The winner is Player " + player + "!"
        winner_text = winner_font.render(winner, True, (220, 150, 0))
        winner_rect = winner_text.get_rect()
        winner_rect.left = (screen_x / 2) - (winner_text.get_width() / 2)
        winner_rect.top = (screen_y / 2) - (winner_text.get_height() / 2)
        screen.blit(winner_text, winner_rect)

        subtitle_font = pygame.font.Font(font_file, 30)
        sub = "Click anywhere to return to main menu"
        text = subtitle_font.render(sub, True, (220, 150, 0))
        rect = text.get_rect()
        rect.left = (screen_x / 2) - (text.get_width() / 2)
        rect.top = (screen_y / 3) * 2 - (text.get_height() / 2)
        screen.blit(text, rect)

        # Look at all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If press quit
                running = False
            if event.type == pygame.KEYDOWN:  # If press key
                if event.key == pygame.K_ESCAPE:  # If key is escape
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse click
                if event.button == 1:  # If left click
                    click = True
                    pygame.mixer.music.load(music_directory + 'main_menu.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.Sound.play(click_sound)

                    # Reset game stats for new game
                    players = [a, b]
                    game.turns = 1
                    for i in players:
                        i.team = [0, 0, 0, 0, 0]
                        i.lives = 10

                    running = False

        pygame.display.update()
        clock.tick(60)
