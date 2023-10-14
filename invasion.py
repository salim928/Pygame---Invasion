import sys

from time import sleep

import pygame
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship

#Creating a Pygame Window and Responding to User Input

"""We’ll make an empty Pygame window by creating a class to represent the 
game. In your text editor, create a new file and save it as alien_invasion.py; 
then enter the following:"""

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings  = Settings()

        # The object we assigned to self.screen is called a surface.
        """Pygame is a part of the screen where a game element can be displayed. 
           Each element in the game, like an alien or a ship, is its own surface."""

        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        """For FullScreen"""
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        

        # self.screen = pygame.display.set_mode((1200,500))
        pygame.display.set_caption("Alien Invasion")
        
        #Create ana instance to store game statistics
        self.stats = GameStats(self)

        #  Create an instance to store game statistics and a scoreboard
        self.sb = Scoreboard(self)


        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Set the background color.
        self.bg_color = (230, 230, 230)

        # Make the Play button.
        self.play_button = Button(self, "Play")

        


        """The game is controlled by the run_game() method. This method contains 
           a while loop w that runs continually. The while loop contains an event loop 
           and code that manages screen updates. An event is an action that the user 
           performs while playing the game, such as pressing a key or moving the 
           mouse. To make our program respond to events, we write this event loop to 
           listen for events and perform appropriate tasks depending on the kinds of 
           events that occur. The for loop at x is an event loop."""

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active: 
               self.ship.update()
               self._update_bullets()
               self._update_aliens()

            
            self._update_screen()
                

            
            # Redraw the screen during each pass through the loop.
            #self.screen.fill(self.bg_color)
            
            
            # Make the most recently drawn screen visible.
            #pygame.display.flip()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            button_click = self.play_button.rect.collidepoint(mouse_pos)
            if button_click and not self.stats.game_active:
            # Reset the game settings
               self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
               self.stats.reset_stats()
               self.stats.game_active = True
               self.sb.prep_score()


            # Get rid of any remaining aliens and bullets.
               self.aliens.empty()
               self.bullets.empty()

            # Create a new fleet and center the ship.
               self._create_fleet()
               self.ship.center_ship()


               # Hide the mouse cursor
               pygame.mouse.set_visible(False)     

    
    #def _start_game(self):
      #  """"""
               
               

    def _check_keydown_events(self,event):
        """Response to keypresses"""
        if event.key == pygame.K_RIGHT:
                    # MOVE THE SHIP TO THE RIGHT
                    #self.ship.rect.x += 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True


    def _check_keyup_events(self, event):
        """Responds to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        #elif event.key == pygame.K_p:
         #   self._check_play_button()


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
           new_bullet = Bullet(self)
           self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

         # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.

        self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
            self.sb.check_high_score()
            self.sb.prep_score()
            self.sb.prep_score()
            self.sb.prep_ships()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()



                
    def _update_aliens(self):
        """
        Check if the fleet is at an edge,then update the positions of all aliens in the fleet.
         """
        self._check_fleet_edges()
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()


        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()




    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
           #Decrement ships_left, and update the scoreboard
           self.stats.ships_left -= 1
           self.sb.prep_ships()

           #Get rid of any remaining alien and bullet
           self.aliens.empty()
           self.bullets.empty()

           #Create a new fleet and center the ship
           self._create_fleet()
           self.ship.center_ship()

           #Pause
           sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this same as if the ship ghot hit
                self._ship_hit()
                break




    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -(3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens.

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
        # Create an alien and place it in the row.
               self._create_alien(alien_number,row_number) 


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1





    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Drew the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
           self.play_button.draw_button()



        # Make the most recently drawn screen visible.
        pygame.display.flip()




if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()






