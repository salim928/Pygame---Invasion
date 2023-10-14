# Creating Settings class for Alien Invasion

"""Each time we introduce new functionality into the game, we’ll typically 
create some new settings as well. Instead of adding settings throughout 
the code, let’s write a module called settings that contains a class called 
Settings to store all these values in one place. This approach allows us to 
work with just one settings object any time we need to access an individual 
setting. This also makes it easier to modify the game’s appearance and 
behavior as our project grows: to modify the game, we’ll simply change 
some values in settings.py, which we’ll create next, instead of searching for 
different settings throughout the project."""

class Settings:
    """A class to store all setttings for Alien Invasion"""
    def __init__(self):
        """Initialize the game settings"""
        #Screen Settings
        self.screen_width = 800
        self.screen_height = 500
        self.bg_color = (255, 255, 255)
        self.bullets_allowed = 3

        #Speed Setting
        self.ship_speed = 1.5
        self.ship_limit = 3

        """Bullet Settings"""

        self.bullet_speed = 1.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # Alien settings
        self.alien_speed = 1.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        



        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien points values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents lefts.
        self.fleet_direction = 1

        # Scoring
        self.alien_point = 50


    def increase_speed(self):
        """Increased speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)
