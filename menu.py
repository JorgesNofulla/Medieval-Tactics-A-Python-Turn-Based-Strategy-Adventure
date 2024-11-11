# menu.py
import pygame
import button
import os
import sys

# Constants
BOTTOM_PANEL = 200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500 + BOTTOM_PANEL
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# Initialize Pygame modules
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battle')

# Load Start Screen Assets
start_screen_background = pygame.image.load(os.path.join(ASSETS_PATH, 'main_menu.png')).convert_alpha()
start_screen_background = pygame.transform.scale(start_screen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Button Images
single_battle_img = pygame.image.load(os.path.join(ASSETS_PATH, 'single_battle.png')).convert_alpha()
tower_of_hell_img = pygame.image.load(os.path.join(ASSETS_PATH, 'tower_of_hell.png')).convert_alpha()

# Create Button Instances
# Adjust the positions (x, y) and sizes (width, height) as needed
single_battle_button = button.Button(screen, 100, 350, single_battle_img, 200, 200)
tower_of_hell_button = button.Button(screen, 500, 350, tower_of_hell_img, 200, 200)

# Hover scale factor for buttons
HOVER_SCALE_FACTOR = 1.1  # 10% larger when hovered

# Load Cursor Image
cursor_img = pygame.image.load(os.path.join(ASSETS_PATH, 'sword.png')).convert_alpha()
cursor_rect = cursor_img.get_rect()

# Font setup for footer
pygame.font.init()
footer_font = pygame.font.SysFont('Arial', 18)
footer_text = "Made by: Jorges Nofulla | Contact: jorgesnofulla12@gmail.com"

def start_screen():
    clicked = False
    while True:
        # Draw Background
        screen.blit(start_screen_background, (0, 0))
        
        pos = pygame.mouse.get_pos()
        
        # Handle Single Battle Button Hover
        if single_battle_button.rect.collidepoint(pos):
            # Scale up the button image
            hover_width = int(single_battle_button.rect.width * HOVER_SCALE_FACTOR)
            hover_height = int(single_battle_button.rect.height * HOVER_SCALE_FACTOR)
            hover_img = pygame.transform.scale(single_battle_img, (hover_width, hover_height))
            
            # Calculate new position to keep the button centered on hover
            hover_x = single_battle_button.rect.centerx - hover_width // 2
            hover_y = single_battle_button.rect.centery - hover_height // 2
            
            # Draw the scaled (hover) button
            screen.blit(hover_img, (hover_x, hover_y))
            
            # Update the rect for the hover image to detect clicks correctly
            hover_rect_single = pygame.Rect(hover_x, hover_y, hover_width, hover_height)
            
            # Handle click on the hover button
            if clicked and hover_rect_single.collidepoint(pos):
                return 'single_battle'  # Return the selected mode
        else:
            # Draw the normal button in its initial position
            single_battle_button.draw()
        
        # Handle Tower of Hell Button Hover
        if tower_of_hell_button.rect.collidepoint(pos):
            # Scale up the button image
            hover_width = int(tower_of_hell_button.rect.width * HOVER_SCALE_FACTOR)
            hover_height = int(tower_of_hell_button.rect.height * HOVER_SCALE_FACTOR)
            hover_img = pygame.transform.scale(tower_of_hell_img, (hover_width, hover_height))
            
            # Calculate new position to keep the button centered on hover
            hover_x = tower_of_hell_button.rect.centerx - hover_width // 2
            hover_y = tower_of_hell_button.rect.centery - hover_height // 2
            
            # Draw the scaled (hover) button
            screen.blit(hover_img, (hover_x, hover_y))
            
            # Update the rect for the hover image to detect clicks correctly
            hover_rect_tower = pygame.Rect(hover_x, hover_y, hover_width, hover_height)
            
            # Handle click on the hover button
            if clicked and hover_rect_tower.collidepoint(pos):
                return 'tower_of_hell'  # Return the selected mode
        else:
            # Draw the normal button in its initial position
            tower_of_hell_button.draw()
        
        # Handle custom cursor for Single Battle and Tower of Hell Buttons
        if single_battle_button.rect.collidepoint(pos) or tower_of_hell_button.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)  # Hide the default cursor
            screen.blit(cursor_img, pos)     # Draw the custom cursor
        else:
            pygame.mouse.set_visible(True)   # Show the default cursor

        # Render and display the footer text
        footer_surface = footer_font.render(footer_text, True, (255, 255, 255))  # White color
        # Center the footer text
        footer_x = (SCREEN_WIDTH - footer_surface.get_width()) // 2
        footer_y = SCREEN_HEIGHT - 30
        screen.blit(footer_surface, (footer_x, footer_y))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        
        pygame.display.update()
