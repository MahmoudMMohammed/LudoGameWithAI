import pygame


class LudoToken:

    def __init__(self, game, color, x, y):

        self.game = game
        self.settings = self.game.settings

        self.color_chooser(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def color_chooser(self, color):
        if color == "red":
            self.image = pygame.image.load(self.settings.RED_TOKEN_PATH).convert()

        elif color == "green":
            self.image = pygame.image.load(self.settings.GREEN_TOKEN_PATH).convert()

        elif color == "blue":
            self.image = pygame.image.load(self.settings.BLUE_TOKEN_PATH).convert()

        elif color == "yellow":
            self.image = pygame.image.load(self.settings.YELLOW_TOKEN_PATH).convert()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_in_base(self):
        # Find the index of the current token in the token group
        try:
            token_index = self.game.player.current_player_token_group.index(self)
        except ValueError:
            # If the token is not in the group, it cannot be in base
            return False

        # Get the placeholder sprite for this token
        placeholder_sprite = self.game.player.current_player_placeholder_group[token_index]

        # Check if the token's position matches the placeholder's position
        if self.rect.x == placeholder_sprite.rect.x and self.rect.y == placeholder_sprite.rect.y:
            return True
        else:
            return False

