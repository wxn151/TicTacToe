import numpy as np
import random
import os
import copy

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

# === Agente con ADN persistente ===
class Agent:
    def __init__(self, dna=None):
        self.dna = np.random.rand(9) if dna is None else dna
        self.fitness = 0

    def get_move(self, board):
        moves = [i for i in range(9) if board[i] == '-']
        if not moves:
            return None
        ranked_moves = sorted(moves, key=lambda x: -self.dna[x])
        return ranked_moves[0]

    def mutate_from_loss(self, human_moves):
        for move in human_moves:
            self.dna[move] -= 0.1
        self.dna += np.random.normal(0, 0.02, size=9)
        self.dna = np.clip(self.dna, 0, 1)

    def save(self, filename="ai_dna.npy"):
        np.save(filename, self.dna)

    @staticmethod
    def load(filename="ai_dna.npy"):
        if os.path.exists(filename):
            dna = np.load(filename)
            print("🧬 AI DNA loaded from file.")
            return Agent(dna)
        else:
            print("⚙️ No saved DNA found. Training new AI...")
            return None

# === Evolución genética ===
def play_game(agent1, agent2):
    game = TicTacToe()
    letter = 'X'
    while game.empty_squares():
        move = agent1.get_move(game.board) if letter == 'X' else agent2.get_move(game.board)
        if move is not None and game.make_move(move, letter):
            if game.current_winner:
                return 1 if letter == 'X' else -1
            letter = 'O' if letter == 'X' else 'X'
    return 0

def evolve(population_size=50, generations=30, mutation_rate=0.1):
    population = [Agent() for _ in range(population_size)]
    for gen in range(generations):
        for agent in population:
            agent.fitness = 0
            for _ in range(5):
                opponent = random.choice(population)
                result = play_game(agent, opponent)
                agent.fitness += result
        population.sort(key=lambda x: x.fitness, reverse=True)
        print(f"Generation {gen+1} | Best fitness: {population[0].fitness}")
        next_gen = population[:10]
        while len(next_gen) < population_size:
            p1, p2 = random.choices(next_gen[:10], k=2)
            child_dna = crossover(p1.dna, p2.dna)
            child_dna = mutate(child_dna, mutation_rate)
            next_gen.append(Agent(child_dna))
        population = next_gen
    return population[0]

def crossover(dna1, dna2):
    return np.array([random.choice([g1, g2]) for g1, g2 in zip(dna1, dna2)])

def mutate(dna, rate):
    return np.array([g + np.random.randn()*0.1 if random.random() < rate else g for g in dna])

# === Juego contra humano con aprendizaje persistente ===
def play_vs_human(ai_agent):
    game = TicTacToe()
    human_letter = input("Choose your letter (X goes first): ").upper()
    while human_letter not in ['X', 'O']:
        human_letter = input("Invalid. Choose X or O: ").upper()
    ai_letter = 'O' if human_letter == 'X' else 'X'
    current_letter = 'X'
    human_moves = []

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
                        human_moves.append(move)
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
            if winner == "You":
                print("AI will learn from this loss...")
                ai_agent.mutate_from_loss(human_moves)
                ai_agent.save()
            elif winner == "AI":
                ai_agent.save()
            return

        current_letter = 'O' if current_letter == 'X' else 'X'

    game.print_board()
    print("It's a draw!")
    ai_agent.save()

# === Ejecutar juego ===
if __name__ == "__main__":
    ai_agent = Agent.load()
    if ai_agent is None:
        ai_agent = evolve()
        ai_agent.save()
        print("AI training complete and saved c[_].")

    print("\n🎮 Let's play Tic Tac Toe!")
    while True:
        play_vs_human(ai_agent)
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            break
