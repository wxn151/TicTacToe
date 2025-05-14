import numpy as np

# === Juego Tic Tac Toe ===
class TicTacToe:
    def __init__(self):
        self.board = ['-' for _ in range(9)]
        self.current_winner = None

    def make_move(self, square, letter):
        if self.board[square] == '-':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == '-']

    def empty_squares(self):
        return '-' in self.board

    def print_board(self):
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            print(" | ".join(row))
            if i < 2:
                print("--+---+--")
        print()

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in col]):
            return True
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0,4,8]]
            if all([s == letter for s in diag1]):
                return True
            diag2 = [self.board[i] for i in [2,4,6]]
            if all([s == letter for s in diag2]):
                return True
        return False

# === Agente con Minimax ===
class Agent:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, board):
        game = TicTacToe()
        game.board = board.copy()
        move = self.minimax(game, self.letter)['position']
        return move

    def minimax(self, game, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # Caso terminal
        if game.current_winner == other_player:
            return {'position': None, 'score': 1 * (len(game.available_moves()) + 1) if other_player == max_player else -1 * (len(game.available_moves()) + 1)}
        elif not game.empty_squares():
            return {'position': None, 'score': 0}

        best = {'position': None, 'score': -np.inf if player == max_player else np.inf}

        for possible_move in game.available_moves():
            game.board[possible_move] = player
            if game.winner(possible_move, player):
                game.current_winner = player
            sim_score = self.minimax(game, other_player)

            # deshacer
            game.board[possible_move] = '-'
            game.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

# === Jugar contra humano ===
def play_vs_human(ai_agent):
    game = TicTacToe()
    human_letter = input("Choose your letter (X goes first): ").upper()
    while human_letter not in ['X', 'O']:
        human_letter = input("Invalid. Choose X or O: ").upper()
    ai_letter = 'O' if human_letter == 'X' else 'X'
    ai_agent.letter = ai_letter
    current_letter = 'X'

    while game.empty_squares():
        print("\nCurrent board:")
        game.print_board()

        if current_letter == human_letter:
            valid = False
            while not valid:
                try:
                    move = int(input(f"Your move (0-8): "))
                    if move in game.available_moves():
                        valid = True
                        game.make_move(move, human_letter)
                    else:
                        print("Invalid move.")
                except:
                    print("Enter a number between 0-8.")
        else:
            move = ai_agent.get_move(game.board)
            print(f"AI plays: {move}")
            game.make_move(move, ai_letter)

        if game.current_winner:
            game.print_board()
            winner = "You" if current_letter == human_letter else "AI"
            print(f"{winner} won the game!")
            return

        current_letter = 'O' if current_letter == 'X' else 'X'

    game.print_board()
    print("It's a draw!")

# === Ejecutar juego ===
if __name__ == "__main__":
    print("\n🎮 Let's play Tic Tac Toe with Minimax AI!")
    ai_agent = Agent(letter='O')  # se asigna correctamente al iniciar el juego
    while True:
        play_vs_human(ai_agent)
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            break
