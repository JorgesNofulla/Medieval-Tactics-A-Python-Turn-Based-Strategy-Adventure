import pygame
import random
import button
import os
from menu import start_screen
pygame.init()
clock = pygame.time.Clock()

# Game settings
FPS = 60
BOTTOM_PANEL = 200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500 + BOTTOM_PANEL

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battle')

# Constants
ACTION_WAIT_TIME = 30
POTION_EFFECT = 15

# Fighter stats
KNIGHT_HP = 35
KNIGHT_STRENGTH = 13
KNIGHT_POTIONS = 3
KNIGHT_BOOSTS = 3
KNIGHT_BOOST_AMOUNT = 5

BANDIT_HP = 30
BANDIT_STRENGTH = 6
BANDIT_POTIONS = 1

# Define fonts and colors
FONT = pygame.font.SysFont('Times New Roman', 26)
RED = (0, 0, 0)
GREEN = (0, 255, 0)

# Hover scale factor for buttons
HOVER_SCALE_FACTOR = 0.5  # 10% larger


# Define the assets folder path
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')



# Load images
background_img = pygame.image.load(os.path.join(ASSETS_PATH, 'backg.png')).convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, 500))

panel_img = pygame.image.load(os.path.join(ASSETS_PATH, 'panel4.png')).convert_alpha()
panel_img = pygame.transform.scale(panel_img, (SCREEN_WIDTH, 200))

potion_img = pygame.image.load(os.path.join(ASSETS_PATH, 'potion.png')).convert_alpha()
boost_img = pygame.image.load(os.path.join(ASSETS_PATH, 'boost.png')).convert_alpha()
restart_img = pygame.image.load(os.path.join(ASSETS_PATH, 'restart.png')).convert_alpha()

victory_img = pygame.image.load(os.path.join(ASSETS_PATH, 'victory.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join(ASSETS_PATH, 'defeat.png')).convert_alpha()

sword_img = pygame.image.load(os.path.join(ASSETS_PATH, 'sword.png')).convert_alpha()

cursor_img = pygame.image.load(os.path.join(ASSETS_PATH, 'sword.png')).convert_alpha()
cursor_rect = cursor_img.get_rect()

# Create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

# Function for drawing panel
def draw_panel():
    screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))
    draw_text(f'{knight.name} HP: {knight.hp}', FONT, RED, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.hp}', FONT, RED, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)

# Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        
        # Set the base path for assets
        base_path = os.path.join(os.path.dirname(__file__), self.name)
        
        # Load idle images
        temp_list = []
        for i in range(3):
            img_path = os.path.join(base_path, 'Idle', f'{i}.png')
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (img.get_width() / 2.5, img.get_height() / 2.5)
                if self.name == 'char'
                else (img.get_width() * 3, img.get_height() * 3),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(2):
            img_path = os.path.join(base_path, 'Attack', f'{i}.png')
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (img.get_width() / 2.5, img.get_height() / 2.5)
                if self.name == 'char'
                else (img.get_width() * 3, img.get_height() * 3),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt images
        temp_list = []
        for i in range(1):
            img_path = os.path.join(base_path, 'Hurt', f'{i}.png')
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (img.get_width() / 2.5, img.get_height() / 2.5)
                if self.name == 'char'
                else (img.get_width() * 3, img.get_height() * 3),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death images
        temp_list = []
        for i in range(1):
            img_path = os.path.join(base_path, 'Death', f'{i}.png')
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (img.get_width() / 2.5, img.get_height() / 2.5)
                if self.name == 'char'
                else (img.get_width() * 3, img.get_height() * 3),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Set initial image and rect position
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        target.hurt()
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        animation_cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = FONT.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

# Create knight and enemies using constants
knight = Fighter(100, 410, 'char', KNIGHT_HP, KNIGHT_STRENGTH, KNIGHT_POTIONS)
enemy1 = Fighter(500, 410, 'Bandit2', BANDIT_HP, BANDIT_STRENGTH, BANDIT_POTIONS)
enemy2 = Fighter(600, 410, 'Bandit2', BANDIT_HP, BANDIT_STRENGTH, BANDIT_POTIONS)

# Initialize knight boosts
knight_boosts = KNIGHT_BOOSTS  # Ensure KNIGHT_BOOSTS is defined before this line

knight_health_bar = HealthBar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40, enemy1.hp, enemy1.max_hp)
bandit2_health_bar = HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 100, enemy2.hp, enemy2.max_hp)

bandit_list = [enemy1, enemy2]

# Create buttons
potion_button = button.Button(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)
boost_button = button.Button(screen, 180, SCREEN_HEIGHT - BOTTOM_PANEL + 70, boost_img, 64, 64)

current_fighter = 1
total_fighters = 3
action_cooldown = 0
attack = False
potion = False
boost = False
clicked = False
game_over = 0
points = 0  # Initialize points globally
friend = None
friend_hired = False


def run_single_battle_mode():
    global knight_boosts
    global game_over
    global current_fighter
    global action_cooldown
    global attack
    global potion
    global boost
    global clicked

    run = True
    while run:
        clock.tick(FPS)
        draw_bg()
        draw_panel()
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(enemy1.hp)
        bandit2_health_bar.draw(enemy2.hp)

        knight.update()
        knight.draw()

        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        damage_text_group.update()
        damage_text_group.draw(screen)

        attack = False
        potion = False
        boost = False
        target = None
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                pygame.mouse.set_visible(False)
                screen.blit(sword_img, pos)
                if clicked and bandit.alive:
                    attack = True
                    target = bandit_list[count]

        if potion_button.draw():
            potion = True

        if boost_button.draw():
            boost = True

        draw_text(str(knight.potions), FONT, RED, 110, SCREEN_HEIGHT - BOTTOM_PANEL + 70)
        draw_text(str(knight_boosts), FONT, GREEN, 190, SCREEN_HEIGHT - BOTTOM_PANEL + 70)

        if game_over == 0:
            if knight.alive:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= ACTION_WAIT_TIME:
                        if attack and target:
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        elif boost:
                            if knight_boosts > 0:
                                knight.strength += KNIGHT_BOOST_AMOUNT
                                knight_boosts -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(KNIGHT_BOOST_AMOUNT), RED)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                        elif potion:
                            if knight.potions > 0:
                                heal_amount = min(POTION_EFFECT, knight.max_hp - knight.hp)
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
            else:
                game_over = -1

            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive:
                        action_cooldown += 1
                        if action_cooldown >= ACTION_WAIT_TIME:
                            if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                heal_amount = min(POTION_EFFECT, bandit.max_hp - bandit.hp)
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                            else:
                                bandit.attack(knight)
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            if current_fighter > total_fighters:
                current_fighter = 1

            alive_bandits = sum(1 for bandit in bandit_list if bandit.alive)
            if alive_bandits == 0:
                game_over = 1

        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
            elif game_over == -1:
                screen.blit(defeat_img, (290, 50))
            if restart_button.draw():
                knight.reset()
                for bandit in bandit_list:
                    bandit.reset()
                current_fighter = 1
                knight_boosts = KNIGHT_BOOSTS  # Reset to initial boost count
                action_cooldown = 0
                game_over = 0

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        pygame.display.update()

    pygame.quit()

def run_tower_of_hell_mode():
    global knight_boosts, game_over, current_fighter, action_cooldown, attack, potion, boost, clicked, points, friend, friend_hired

    # Initialize Tower of Hell variables
    level = 1
    max_levels = 10
    points = 0  # Points earned, will be saved even after death
    friend_hired = False  # Flag to check if friend is hired
    friend = None  # Initialize friend to None

    # Function to create enemies based on the current level
    def create_enemies(level):
        enemies = []
        for i in range(level):
            enemy = Fighter(500 + i * 100, 410, 'Bandit2', BANDIT_HP, BANDIT_STRENGTH, BANDIT_POTIONS)
            enemies.append(enemy)
        return enemies

    # Function to handle the store
    def open_store():
        global knight, friend_hired, friend, points
        store_open = True
        while store_open:
            clock.tick(FPS)
            draw_bg()
            draw_text("STORE", FONT, RED, SCREEN_WIDTH // 2 - 40, 50)
            draw_text(f"Points: {points}", FONT, GREEN, SCREEN_WIDTH // 2 - 60, 100)
            draw_text("1. Increase Health (+10) - 30 points", FONT, RED, 100, 200)
            draw_text("2. Buy Weapon (+5 Strength) - 50 points", FONT, RED, 100, 250)
            if not friend_hired:
                draw_text("3. Hire Friend - 100 points", FONT, RED, 100, 300)
            else:
                draw_text("Friend Hired", FONT, GREEN, 100, 300)
            draw_text("Press the number key to purchase or 'N' to continue", FONT, RED, 100, 400)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and points >= 30:
                        knight.max_hp += 10
                        knight.hp += 10
                        points -= 30
                    elif event.key == pygame.K_2 and points >= 50:
                        knight.strength += 5
                        points -= 50
                    elif event.key == pygame.K_3 and points >= 100 and not friend_hired:
                        # Hire friend
                        friend = Fighter(300, 410, 'Bandit', 30, 8, 0)
                        friend_hired = True
                        points -= 100
                    elif event.key == pygame.K_n:
                        store_open = False

    while level <= max_levels:
        # Reset game_over and other variables for the new level
        game_over = 0
        current_fighter = 1
        action_cooldown = 0
        attack = False
        potion = False
        boost = False
        clicked = False

        # Create enemies for the current level
        enemies = create_enemies(level)
        bandit_list = enemies  # Update bandit_list to current enemies

        # Initialize health bars
        knight_health_bar = HealthBar(100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
        enemy_health_bars = [
            HealthBar(550, SCREEN_HEIGHT - BOTTOM_PANEL + 40 + i * 60, enemy.hp, enemy.max_hp)
            for i, enemy in enumerate(enemies)
        ]
        if friend_hired:
            friend_health_bar = HealthBar(300, SCREEN_HEIGHT - BOTTOM_PANEL + 40, friend.hp, friend.max_hp)

        run = True
        while run:
            clock.tick(FPS)
            draw_bg()
            draw_panel()
            knight_health_bar.draw(knight.hp)
            for i, hb in enumerate(enemy_health_bars):
                hb.draw(bandit_list[i].hp)
            if friend_hired:
                friend_health_bar.draw(friend.hp)

            knight.update()
            knight.draw()
            if friend_hired:
                friend.update()
                friend.draw()

            for bandit in bandit_list:
                bandit.update()
                bandit.draw()

            damage_text_group.update()
            damage_text_group.draw(screen)

            attack = False
            potion = False
            boost = False
            target = None
            pygame.mouse.set_visible(True)
            pos = pygame.mouse.get_pos()
            for count, bandit in enumerate(bandit_list):
                if bandit.rect.collidepoint(pos):
                    pygame.mouse.set_visible(False)
                    screen.blit(sword_img, pos)
                    if clicked and bandit.alive:
                        attack = True
                        target = bandit_list[count]

            if potion_button.draw():
                potion = True

            if boost_button.draw():
                boost = True

            draw_text(str(knight.potions), FONT, RED, 110, SCREEN_HEIGHT - BOTTOM_PANEL + 70)
            draw_text(str(knight_boosts), FONT, GREEN, 190, SCREEN_HEIGHT - BOTTOM_PANEL + 70)

            if game_over == 0:
                # Increment action cooldown every loop
                action_cooldown += 1

                # Handle turn order
                if current_fighter == 1:
                    # Knight's turn
                    if knight.alive:
                        if action_cooldown >= ACTION_WAIT_TIME:
                            if attack and target:
                                knight.attack(target)
                                action_cooldown = 0
                                current_fighter += 1
                            elif potion:
                                if knight.potions > 0:
                                    heal_amount = min(POTION_EFFECT, knight.max_hp - knight.hp)
                                    knight.hp += heal_amount
                                    knight.potions -= 1
                                    damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), GREEN)
                                    damage_text_group.add(damage_text)
                                    action_cooldown = 0
                                    current_fighter += 1
                            elif boost:
                                if knight_boosts > 0:
                                    knight.strength += KNIGHT_BOOST_AMOUNT
                                    knight_boosts -= 1
                                    damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(KNIGHT_BOOST_AMOUNT), RED)
                                    damage_text_group.add(damage_text)
                                    action_cooldown = 0
                                    current_fighter += 1
                            elif clicked == False and (not attack) and (not potion) and (not boost):
                                # Wait for player to take an action
                                pass
                            else:
                                # No valid action, pass turn
                                action_cooldown = 0
                                current_fighter += 1
                    else:
                        # Knight is dead
                        game_over = -1
                elif current_fighter == 2 and friend_hired:
                    # Friend's turn
                    if friend.alive:
                        if action_cooldown >= ACTION_WAIT_TIME:
                            alive_enemies = [enemy for enemy in bandit_list if enemy.alive]
                            if alive_enemies:
                                target = random.choice(alive_enemies)
                                friend.attack(target)
                            action_cooldown = 0
                            current_fighter += 1
                        else:
                            # Wait for action cooldown
                            pass
                    else:
                        # Friend is dead
                        current_fighter += 1
                else:
                    # Enemies' turns
                    enemy_index = current_fighter - (2 if friend_hired else 1)
                    if 0 <= enemy_index < len(bandit_list):
                        enemy = bandit_list[enemy_index]
                        if enemy.alive:
                            if action_cooldown >= ACTION_WAIT_TIME:
                                # Enemy's action
                                if friend_hired and friend.alive:
                                    target = random.choice([knight, friend])
                                else:
                                    target = knight
                                enemy.attack(target)
                                action_cooldown = 0
                                current_fighter += 1
                            else:
                                # Wait for action cooldown
                                pass
                        else:
                            # Enemy is dead
                            current_fighter += 1
                    else:
                        # Reset turn order
                        current_fighter = 1

                # Check if all enemies are defeated
                alive_enemies = [enemy for enemy in bandit_list if enemy.alive]
                if len(alive_enemies) == 0:
                    game_over = 1

            if game_over != 0:
                if game_over == 1:
                    screen.blit(victory_img, (250, 50))
                    draw_text("Press 'N' for next level or 'S' to open store", FONT, RED, 200, 200)
                    pygame.display.update()
                    level_completed = False
                    while not level_completed:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_n:
                                    level += 1
                                    points += level * 10  # Award points
                                    level_completed = True
                                    # Reset buffs and potions
                                    knight_boosts = KNIGHT_BOOSTS
                                    knight.potions = KNIGHT_POTIONS
                                    if friend_hired:
                                        friend.reset()
                                    run = False
                                elif event.key == pygame.K_s:
                                    open_store()
                                    level_completed = True
                                    # After shopping, proceed to next level
                                    level += 1
                                    points += level * 10
                                    knight_boosts = KNIGHT_BOOSTS
                                    knight.potions = KNIGHT_POTIONS
                                    if friend_hired:
                                        friend.reset()
                                    run = False
                elif game_over == -1:
                    screen.blit(defeat_img, (290, 50))
                    draw_text("Press 'R' to restart or 'S' to open store", FONT, RED, 200, 200)
                    pygame.display.update()
                    game_over_handled = False
                    while not game_over_handled:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    level = 1
                                    knight.reset()
                                    knight_boosts = KNIGHT_BOOSTS
                                    knight.potions = KNIGHT_POTIONS
                                    if friend_hired:
                                        friend.reset()
                                    game_over_handled = True
                                    run = False
                                elif event.key == pygame.K_s:
                                    open_store()
                                    # Restart from level 1 after shopping
                                    level = 1
                                    knight.reset()
                                    knight_boosts = KNIGHT_BOOSTS
                                    knight.potions = KNIGHT_POTIONS
                                    if friend_hired:
                                        friend.reset()
                                    game_over_handled = True
                                    run = False

            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            pygame.display.update()

    # Game completed
    draw_text("Congratulations! You've completed the Tower!", FONT, GREEN, 150, 200)
    draw_text(f"Total Points: {points}", FONT, GREEN, 250, 250)
    pygame.display.update()
    pygame.time.delay(5000)






# Start the game
game_mode = start_screen()  # Get the selected game mode

if game_mode == 'single_battle':
    run_single_battle_mode()
elif game_mode == 'tower_of_hell':
    run_tower_of_hell_mode()  # Change this to the correct function when implemented
else:
    print("Unknown game mode selected!")
    pygame.quit()