import random
import time

import pygame
import sys

from player import AIPlayer
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
        self.ai_player = AIPlayer(self, "red")
        self.player = Player(self)
        self.board = Board(self)
        self.events = Events(self)
        self.dice = Dice(self)

    def start_ai_game(self):
        # Initialize players
        self.player.color_for_player = ["red", "yellow"]  # Red for AI, Yellow for human
        self.player.no_of_players = 2
        self.player.initialize_players()

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
                self.dice.roll_dice()
                self.dice.dice_val = self.dice.get_dice_val()

                print(f"got roll: {self.dice.dice_val}")

                # Choose the best token to move
                best_move = self.ai_player.choose_best_move()

                if best_move is not None:

                    dice_value = self.dice.get_dice_val()

                    # Set the token selector to the chosen token
                    self.events.token_selector = best_move
                    self.events.ludo_token = self.player.current_player_token_group[best_move]

                    # Determine if the token should move on the normal path or winning path
                    check_path, check_val = self.player.check_ai_move(self.events.token_selector)
                    print(f"path: {check_path}")
                    print(f"val: {check_val}")

                    if check_path == 0:
                        self.menu.skipped_turn_text = "Dice value less than 6, turn skipped..."
                        self.menu.is_turn_skip = True
                        self.dice.dice_reset()

                    if check_path == 1:
                        # Move on the normal path
                        self.player.move_on_normal_path_ai()
                        print(f"AI moved token {best_move+1} on normal path, with dice roll {dice_value}.")

                    if check_path == 2:
                        # Move on the winning path
                        self.player.move_on_winning_path_ai()
                        print(f"AI moved token {best_move+1} on winning path, with dice roll {dice_value}.")

                    if check_path == 6:
                        self.player.current_player_on_start_path()
                    print("---------------------------------------")

                else:
                    print("No movable tokens!")
                    print("---------------------------------------")
            time.sleep(1)


            # Switch to the next player (human)
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

            # Draw all the objects onto their respective places
            self.draw_sprites()

            # Update window with new sprite positions of the objects
            pygame.display.flip()
