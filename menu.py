import pygame
import random
import button
import os
BOTTOM_PANEL = 200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500 + BOTTOM_PANEL
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# Start screen
start_screen_background = pygame.image.load(os.path.join(ASSETS_PATH, 'main_menu.png')).convert_alpha()
start_screen_background = pygame.transform.scale(start_screen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_button_img = pygame.image.load(os.path.join(ASSETS_PATH, 'sb.png')).convert_alpha()
start_button = button.Button(screen, 300, 350, start_button_img, 200, 200)

# Hover scale factor for buttons
HOVER_SCALE_FACTOR = 0.5  # 10% larger
cursor_img = pygame.image.load(os.path.join(ASSETS_PATH, 'sword.png')).convert_alpha()
cursor_rect = cursor_img.get_rect()

# Font setup for footer
pygame.font.init()
footer_font = pygame.font.SysFont('Arial', 18)
footer_text = "Made by: Jorges Nofulla | Contact: jorgesnofulla12@gmail.com"

def start_screen():
    clicked = False
    while True:
        screen.blit(start_screen_background, (0, 0))
        
        pos = pygame.mouse.get_pos()
        
        # Get button dimensions directly from the image
        button_width, button_height = start_button_img.get_width(), start_button_img.get_height()
        
        # Check if the mouse is over the start button
        if start_button.rect.collidepoint(pos):
            # Scale up the button image
            hover_width = int(button_width * HOVER_SCALE_FACTOR)
            hover_height = int(button_height * HOVER_SCALE_FACTOR)
            hover_img = pygame.transform.scale(start_button_img, (hover_width, hover_height))
            
            # Calculate new position to keep the button centered on hover
            hover_x = start_button.rect.centerx - hover_width // 2
            hover_y = start_button.rect.centery - hover_height // 2
            
            # Draw the scaled (hover) button
            screen.blit(hover_img, (hover_x, hover_y))
            
            # Update the rect for the hover image to detect clicks correctly
            hover_rect = pygame.Rect(hover_x, hover_y, hover_width, hover_height)
            
            # Handle click on the hover button
            if clicked and hover_rect.collidepoint(pos):
                break  # Start the game
        else:
            # Draw the normal button in its initial position
            if start_button.draw():
                break  # Start the game
        
        # Handle custom cursor
        if start_button.rect.collidepoint(pos):
            pygame.mouse.set_visible(False)  # Hide the default cursor
            screen.blit(cursor_img, pos)     # Draw the custom cursor
        else:
            pygame.mouse.set_visible(True)   # Show the default cursor

        # Render and display the footer text
        footer_surface = footer_font.render(footer_text, True, (255, 255, 255))  # White color
        screen.blit(footer_surface, (SCREEN_WIDTH // 4 - footer_surface.get_width() // 2, SCREEN_HEIGHT - 30))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        
        pygame.display.update()
