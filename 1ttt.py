import math
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'

    def print_board(self):
        print("\nCurrent Board:")
        for row in range(3):
            print(" " + " | ".join(self.board[row * 3:(row + 1)* 3]))
            if row < 2:
                print("---|---|---")
        print()

    def available_moves(self):
        return[i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            return True
        return False

    def check_winner(self, board, player):
        # Winning combinations: 3 rows, 3 columns, 2 diagonals
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for condition in win_conditions:
            if all(board[i] == player for i in condition):
                return True
        return False

    def minimax(self, state, is_maximizing):
        # Terminal checks
        if self.check_winner(state, self.ai):
            return {'score': 10}
        elif self.check_winner(state, self.human):
            return {'score': -10}
        elif not self.empty_squares():
            return {'score': 0}

        if is_maximizing:
            best = {'score': -math.inf, 'position': None}
            for move in self.available_moves():
                state[move] = self.ai
                sim_score = self.minimax(state, False)
                state[move] = ' '  # Backtrack

                if sim_score['score'] > best['score']:
                    best['score'] = sim_score['score']
                    best['position'] = move
            return best
        else:
            best = {'score': math.inf, 'position': None}
            for move in self.available_moves():
                state[move] = self.human
                sim_score = self.minimax(state, True)
                state[move] = ' '  # Backtrack

                if sim_score['score'] < best['score']:
                    best['score'] = sim_score['score']
                    best['position'] = move
            return best

    def play(self):
        print("Positions are numbered 0 through 8 like this:")
        print(" 0 | 1 | 2 \n---|---|---\n 3 | 4 | 5 \n---|---|---\n 6 | 7 | 8\n")

        current_turn = 'X'  # Human starts first

        while self.empty_squares():
            if current_turn == self.human:
                self.print_board()
                move = None
                while move not in self.available_moves():
                    try:
                        move = int(input("Enter position (0-8): "))
                    except ValueError:
                        continue
                self.make_move(move, self.human)
                current_turn = self.ai
            else:
                print("AI is making a move...")
                move = self.minimax(self.board, True)['position']
                self.make_move(move, self.ai)
                current_turn = self.human

            if self.check_winner(self.board, self.human):
                self.print_board()
                print("Congratulations! You won!")
                return
            elif self.check_winner(self.board, self.ai):
                self.print_board()
                print("AI wins! Better luck next time.")
                return

        self.print_board()
        print("It's a draw!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play()
