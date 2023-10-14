"""Now we need to figure out exactly what will happen when an alien collides 
with the ship. Instead of destroying the ship instance and creating a new 
one, we’ll count how many times the ship has been hit by tracking statistics 
for the game. Tracking statistics will also be useful for scoring.
Let’s write a new class, GameStats, to track game statistics"""


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # Start Alie Invasion in an active state
        # self.game_active = True

        # High score should never be reset.
        self.high_score = 0


    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

