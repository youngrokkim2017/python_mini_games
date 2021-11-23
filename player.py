import math
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # want players to get their next move given a game
    def get_move(self, game):
        pass

# inheritance to get computer player and player
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        #  choose random spot
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-9):')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid swuare. Try again')
        return val

# minimax
class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else: 
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter    #yourself
        other_player = 'O' if player == 'X' else 'X'    # the other player

        #  check if previous move is winner
        # recursion base case
        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
            }
        elif not state.empty_squares():     # no empty squares
            return {
                'position': None,
                'score': 0
            }
        
        if player == max_player:
            best = {
                'position': None,
                'score': -math.inf
            }
        else:
            best = {
                'position': None,
                'score': math.inf
            }

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game after that move
            simulated_score = self.minimax(state, other_player)

            # step 3: undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            simulated_score['position'] = possible_move

            # step 4: update the dictionaries if necessary
            if player == max_player:
                if simulated_score['score'] > best['score']:
                    best = simulated_score
            else:
                if simulated_score['score'] < best['score']:
                    best = simulated_score
            
        return best