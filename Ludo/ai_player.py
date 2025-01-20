import random
from copy import deepcopy

from events import Events


class AIPlayer:
    def __init__(self, game, color):
        self.game = game
        self.color = color

    def choose_best_move(self):
        """
        Choose the best token to move using the Expectiminimax algorithm with a heuristic evaluation.
        """
        best_move = None
        best_score = float('-inf')

        for token_index in range(len(self.game.player.token_sprite_list[self.color])):
            if self.can_move_token(token_index):
                simulated_state = self.get_simulated_state()
                self.simulate_move(simulated_state, token_index)

                score = self.expectiminimax(simulated_state, depth=2, maximizing_player=False)
                if score > best_score:
                    best_score = score
                    best_move = token_index

        return best_move

    def can_move_token(self, token_index):
        token_path_index = self.game.player.token_path_indice[self.color][token_index]
        dice_value = self.game.dice.dice_val
        return token_path_index + dice_value < len(self.game.player.team_path[self.color])

    def simulate_move(self, state, token_index):
        """
        Simulate moving a token for the AI in the given state.
        """
        dice_value = state["dice_val"]
        current_path_index = state["token_path_indice"][self.color][token_index]
        new_path_index = current_path_index + dice_value

        state["token_path_indice"][self.color][token_index] = new_path_index
        state["token_movement_counter"][self.color][token_index] += dice_value

    def heuristic(self, state):
        """
        Evaluate the game state to guide the AI's decision.
        """
        score = 0
        for path_index in state["token_path_indice"][self.color]:
            score += path_index  # Reward tokens closer to the goal

        return score

    def expectiminimax(self, state, depth, maximizing_player):
        """
        Perform the Expectiminimax algorithm using the minimal state.
        """
        if depth == 0:
            return self.heuristic(state)

        if maximizing_player:
            max_eval = float('-inf')
            for token_index in range(len(state["token_path_indice"][self.color])):
                if self.can_move_token(token_index):
                    simulated_state = deepcopy(state)
                    self.simulate_move(simulated_state, token_index)
                    eval = self.expectiminimax(simulated_state, depth - 1, False)
                    max_eval = max(max_eval, eval)
            return max_eval

        else:
            # Simulate the opponent's moves
            min_eval = float('inf')
            for dice_val in range(1, 7):  # Assume uniform dice roll distribution
                simulated_state = deepcopy(state)
                simulated_state["dice_val"] = dice_val
                opponent_color = "yellow"
                for token_index in range(len(simulated_state["token_path_indice"][opponent_color])):
                    if simulated_state["token_path_indice"][opponent_color][token_index] + dice_val < len(
                            simulated_state["token_path_indice"][opponent_color]):
                        simulated_state["token_path_indice"][opponent_color][token_index] += dice_val
                        eval = self.heuristic(simulated_state)
                        min_eval = min(min_eval, eval)
            return min_eval

    def get_simulated_state(self):
        """
        Returns a minimal copy of the game state relevant to the AI's decision-making.
        """
        return {
            "token_path_indice": deepcopy(self.game.player.token_path_indice),
            "token_movement_counter": deepcopy(self.game.player.token_movement_counter),
            "dice_val": self.game.dice.dice_val,
        }
