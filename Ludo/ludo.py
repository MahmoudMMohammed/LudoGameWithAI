import random

import pygame
import sys

from Ludo.ai_player import AIPlayer
from settings import Settings
from board import Board
from dice import Dice
from player import Player
from menu import Menu
from events import Events


class Ludo:

    def __init__(self):
        pygame.init()

        self.settings = Settings(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Ludo")

        # Load the icon image
        icon_image = pygame.image.load("images/ludo_icon.png")
        icon_image = icon_image.convert_alpha()  # Use convert_alpha() for transparency

        # Set the icon
        pygame.display.set_icon(icon_image)

        self.menu = Menu(self)
        self.player = Player(self)
        self.board = Board(self)
        self.events = Events(self)
        self.dice = Dice(self)

        # Initialize AI player
        self.ai_player = None

    def start_ai_game(self):
        # Initialize players
        self.player.color_for_player = ["red", "yellow"]  # Red for AI, Yellow for human
        self.player.no_of_players = 2
        self.player.initialize_players()

        # Create AI player
        self.ai_player = AIPlayer(self, "red")

        # Set the current player to the human player (yellow)
        self.player.current_player = 1
        self.player.current_player_properties_initialization()

        # Start the game loop
        self.run_ai_game()

    def run_ai_game(self):
        while True:
            self.screen.fill(self.settings.board_menu_bg_color)

            # Displays all the buttons on the screen
            self.menu.show_buttons_on_board_menu()

            # Checks all the inputs for making a move on the board menu
            self._check_events()

            # Check if it's the AI's turn
            if self.player.current_player_color == "red":
                # Roll the dice for the AI
                self.dice.roll_dice()

                # Choose the best token to move
                best_move = self.ai_player.choose_best_move()
                if best_move is not None:
                    # Check if the token is on the winning path or normal path
                    token_index = best_move
                    token_path_index = self.player.token_path_indice["red"][token_index]
                    dice_value = self.dice.dice_val

                    # Get a list of movable tokens
                    movable_tokens = []
                    for token_index, path_index in enumerate(self.player.token_path_indice["red"]):
                        if path_index + dice_value < len(self.player.team_path["red"]):
                            movable_tokens.append(token_index)

                    if movable_tokens:
                        # Randomly select a token from the movable tokens
                        selected_token = random.choice(movable_tokens)

                        # Set the token selector to the chosen token
                        self.events.token_selector = selected_token

                        # Determine if the token should move on the normal path or winning path
                        token_path_index = self.player.token_path_indice["red"][selected_token]
                        if token_path_index + dice_value >= self.settings.total_movement_steps:
                            # Move on the winning path
                            self.player.move_on_winning_path()
                        else:
                            # Move on the normal path
                            self.player.move_on_normal_path()

                        print(f"AI moved token {selected_token} with dice roll {dice_value}.")

            # # Switch to the next player (human)
            # self.player.change_current_player()

            # Draw all the objects onto their respective places
            self.draw_sprites()

            # Update window with new sprite positions of the objects
            pygame.display.flip()

    def initialize(self):
        "Initializes all the game elements before it starts"

        self.settings.load_data()
        self.board.load_board()
        self.board.load_board_features()

        self.menu.initialize_main_menu()
        self.menu.initialize_third_menu()
        self.menu.initialize_final_menu()

        self.menu.main_menu()
        self.menu.second_menu()
        self.menu.third_menu()

        self.player.initialize_players()

    def _check_events(self):
        "General function for handling of all inputs."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                self.events.check_mouse_main_menu_event(event.type)
                self.events.check_mouse_second_menu_event(event.type)
                self.events.check_mouse_third_menu_event(event.type)
                self.events.check_mouse_board_menu_event(event.type)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.events.check_mouse_main_menu_event(event.type)
                self.events.check_mouse_second_menu_event(event.type)
                self.events.check_mouse_third_menu_event(event.type)
                self.events.check_mouse_board_menu_event(event.type)


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.events.check_keyboard_final_menu_event()

    def draw_sprites(self):
        "General function for drawing all sprites onto the screen."

        # Draws all the path tiles (movement and winning path tiles)
        self.board.draw_path_tiles(self.screen)
        self.board.draw_winning_path_tiles(self.screen)

        # Draws all blank sprites where tokens can't go
        self.board.blank_sprites.draw(self.screen)

        # Draw the base backgrounds
        self.screen.blit(self.board.base_background, self.settings.base_background_coordinates)
        self.board.draw_placeholder_path_tiles(self.screen)

        # Draw all the tokens
        self.player.draw_tokens_on_board(self.screen)

        # Draws any path highlights for tokens
        self.board.draw_path_highlights(self.screen)

        # Draw the borders
        self.screen.blit(self.board.gridlines, self.settings.grid_and_borders_coordinates)

        # Draw the dungeon
        self.screen.blit(self.board.dungeon, self.settings.dungeon_coordinates)

    def run_game(self):
        while True:
            self.screen.fill(self.settings.board_menu_bg_color)

            # Displays all the buttons on the screen
            self.menu.show_buttons_on_board_menu()

            # Checks all the inputs for making a move on the board menu
            self._check_events()

            # If it's the AI's turn, make a move
            if self.player.current_player == 1 and self.ai_player:
                self.ai_player.make_move()
                self.player.change_current_player()

            # Draw all the objects onto their respective places
            self.draw_sprites()

            # Update window with new sprite positions of the objects
            pygame.display.flip()
