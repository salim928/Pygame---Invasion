# CREATING THE SHIP CLASS

"""After choosing an image for the ship, we need to display it on the screen. To 
use our ship, we’ll create a new ship module that will contain the class Ship. 
This class will manage most of the behavior of the player’s ship:"""

import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    """A class to manage ship"""
    def __init__(self,ai_game):
        """Initialize the ship and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


       

    #Load the ship image and getit rect
        #path = r"C:\Users\LAPTOP\Desktop\Codes\PYTHON\Invasion\images"
        #self.image = pygame.image.load(path)
        self.image = pygame.image.load(r"C:\Users\LAPTOP\Desktop\Documents\Codes\PYTHON\Invasion\images\don.bmp")
        self.rect = self.image.get_rect()

    # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom


     # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)


        #Movement flag
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        #if self.moving_right:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #self.rect. x += 1
            self.x += self.settings.ship_speed
        #elif self.moving_left:
        if self.moving_left and self.rect.left > 0:
            #self.rect.x -= 1
            self.x -= self.settings.ship_speed



        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at it's current location"""
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)