import pygame
import random
import button

pygame.init()
# put a constant fps
clock = pygame.time.Clock()

fps = 60

# The screen 
bottom_panel = 200
screen_Width = 800
screen_height = 500 + bottom_panel

screen = pygame.display.set_mode((screen_Width,screen_height))
pygame.display.set_caption('Battle')

#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
boost = False
potion_effect = 15
knight_boosts = 3  # Set the initial number of attack boosts available for the knight
knight_boost_amount = 5  # Amount of attack boost per use
clicked = False
game_over = 0


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (0, 0, 0)
green = (0, 255, 0)

# start screen
start_screen_background = pygame.image.load('C:/DevOps/Code/assets/main_menu.png').convert_alpha()
start_screen_background = pygame.transform.scale(start_screen_background, (screen_Width, screen_height))
start_button_img = pygame.image.load('C:/DevOps/Data/battle_g/sb.png').convert_alpha()  # Load your start button image
start_button = button.Button(screen, 300, 350, start_button_img, 200, 200)  # Adjust x_position, y_position, width, and height

#load images
#background image

background_img = pygame.image.load('C:/DevOps/Data/battle_g/backg.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_Width, 500))
# Panel (down) image 
panel_img = pygame.image.load('C:/DevOps/Data/battle_g/panel4.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen_Width, 200))
#button images
potion_img = pygame.image.load('C:/DevOps/Data/battle_g/potion.png').convert_alpha()
boost_img = pygame.image.load('C:/DevOps/Data/battle_g/boost.png').convert_alpha()  # Replace with the path to your boost button image
restart_img = pygame.image.load('C:/DevOps/Data/battle_g/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('C:/DevOps/Data/battle_g/victory.png').convert_alpha()
defeat_img = pygame.image.load('C:/DevOps/Data/battle_g/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('C:/DevOps/Data/battle_g/sword.png').convert_alpha()
#create function for drawing text
cursor_img = pygame.image.load('C:/DevOps/Data/battle_g/sword.png').convert_alpha()
cursor_rect = cursor_img.get_rect()



#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	for count, i in enumerate(bandit_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)


# create fighter class

class FIghter():
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
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # Load idle images
        temp_list = []  
        for i in range(3): # prolly needs to automize this too
            if f'{self.name}'=='char':
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Idle/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
                temp_list.append(img)
            else :
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Idle/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()* 3, img.get_height()* 3)) 
                temp_list.append(img)
        self.animation_list.append(temp_list)
        # Load attack
        temp_list = []
        for i in range(2): # prolly needs to automize this too
            if f'{self.name}'=='char':
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Attack/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
                temp_list.append(img)
            else:   
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Attack/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(1): # prolly needs to automize this too
            if f'{self.name}'=='char':
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Hurt/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
                temp_list.append(img)
            else:   
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Hurt/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(1): # prolly needs to automize this too
            if f'{self.name}'=='char':
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Death/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
                temp_list.append(img)
            else:   
                img = pygame.image.load(f'C:/DevOps/Data/battle_g/{self.name}/Death/{i}.png') # this is the idle movement, put the folder
                #img = pygame.image.load(f'C:/DevOps/Data/battle_g/char/Heavy Bandit/Idle/{i}.png')
                img= pygame.transform.scale(img, (img.get_width()*3, img.get_height()*3))
                temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def idle(self):
        #set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animation
        target.hurt()
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        #damage text
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def hurt(self):
        #set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset (self):
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
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
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
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()

def start_screen():
    clicked = False
    while True:
        screen.blit(start_screen_background, (0, 0))

        # Draw start button
        if start_button.draw():
            break

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button and change the cursor
        if start_button.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)  # Hide the default mouse cursor
            screen.blit(cursor_img, pos)  # Draw custom cursor at mouse position
        else:
            pygame.mouse.set_visible(True)  # Show the default mouse cursor

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(pos):
                clicked = True

        pygame.display.update()





damage_text_group = pygame.sprite.Group()

knight = FIghter(100, 410 , 'char', 30, 12, 3)  # Pos, pos, name, HP, str, poition
enemy1 = FIghter(500, 410 , 'Bandit', 30, 6, 1) # this is for automization, for later
enemy2 = FIghter(600, 410 , 'Bandit', 30, 6, 1) # need bandits here

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, enemy2.hp, enemy2.max_hp)

bandit_list = []
bandit_list.append(enemy1)
bandit_list.append(enemy2)
#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)
boost_button = button.Button(screen, 180, screen_height - bottom_panel + 70, boost_img , 64, 64)

start_screen()  # Call this before entering the main game loop
run = True
while run:
    clock.tick(fps)
    #draw background
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

    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)


    #control player actions
    #reset action variables
    attack = False
    potion = False
    boost = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    
    if potion_button.draw():
        potion = True
    # inside your main game loop, within the player action section

    if boost_button.draw():
        boost = True




    #show number of potions remaining
    draw_text(str(knight.potions), font, red, 110, screen_height - bottom_panel + 70)
    #show number of potions remaining
    draw_text(str(knight_boosts), font, green, 190, screen_height - bottom_panel + 70)

    if game_over==0 : 
            #player action
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                                    #potion
                    if boost== True:
                        if knight_boosts > 0:
                            knight.strength += knight_boost_amount
                            knight_boosts -= 1  # Decrement the number of available boosts
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(knight_boost_amount), red)
                            damage_text_group.add(damage_text)
                            current_fighter += 1  # Move to the next fighter
                            action_cooldown = 0  # Reset action cooldown
                             
                    if potion == True:
                        if knight.potions > 0:
                            #check if the potion would heal the player beyond max health
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over=-1

        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #check if bandit needs to heal first
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            #check if the potion would heal the bandit beyond max health
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        #attack
                        else:
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        #if all fighters have had a turn then reset
        if current_fighter > total_fighters:
            current_fighter = 1

        #check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1


    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            knight_boosts = 3
            action_cooldown
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False


    pygame.display.update()

pygame.quit()


#Hi.  I was wondering if it that can be expanded a bit with characters actually moving to each other for interactions?

