import tkinter as tk
from tkinter import messagebox
import random

# Color palette
BG_COLOR = "#2E2E2E"
BUTTON_BG = "#1A1A1A"
X_COLOR = "#00FF87"  # Neon green
O_COLOR = "#FF006E"   # Neon pink
TEXT_COLOR = "#FFFFFF"
STATUS_BG = "#3D3D3D"

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe vs AI")
        self.window.configure(bg=BG_COLOR)
        self.current_player = 'X'
        self.board = [' '] * 9
        self.buttons = []

        # Create game board buttons
        for i in range(9):
            row = i // 3
            col = i % 3
            button = tk.Button(self.window, text=' ', font=('Arial', 32, 'bold'),
                              bg=BUTTON_BG, fg=TEXT_COLOR, width=3, height=1,
                              command=lambda i=i: self.player_click(i))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.buttons.append(button)

        # Add status label
        self.status_label = tk.Label(self.window, text="Your Turn (X)", font=('Arial', 14),
                                    bg=STATUS_BG, fg=TEXT_COLOR, padx=10, pady=5)
        self.status_label.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Configure grid weights
        for i in range(3):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)

    def player_click(self, position):
        if self.board[position] == ' ' and self.current_player == 'X':
            self.make_move(position, 'X')
            if not self.check_game_over():
                self.current_player = 'O'
                self.status_label.config(text="AI Thinking...")
                self.window.after(500, self.ai_move)

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        self.make_move(best_move, 'O')
        self.current_player = 'X'
        self.status_label.config(text="Your Turn (X)")

    def minimax(self, board, depth, is_maximizing):
        scores = {'X': -1, 'O': 1, 'tie': 0}

        result = self.check_winner(board)
        if result in scores:
            return scores[result]

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def make_move(self, position, player):
        self.board[position] = player
        color = X_COLOR if player == 'X' else O_COLOR
        self.buttons[position].config(text=player, fg=color, state=tk.DISABLED)
        self.check_game_over()

    def check_winner(self, board):
        # Check rows
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] != ' ':
                return board[i]
        # Check columns
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != ' ':
                return board[i]
        # Check diagonals
        if board[0] == board[4] == board[8] != ' ':
            return board[0]
        if board[2] == board[4] == board[6] != ' ':
            return board[2]
        # Check tie
        if ' ' not in board:
            return 'tie'
        return None

    def check_game_over(self):
        result = self.check_winner(self.board)
        if result:
            self.end_game(result)
            return True
        return False

    def end_game(self, result):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

        if result == 'X':
            messagebox.showinfo("Game Over", "Congratulations! You won!")
            self.window.destroy()
        elif result == 'O':
            answer = messagebox.askyesno("Game Over", "AI won! Play again?", 
                                       icon='warning')
            if answer:
                self.reset_game()
            else:
                self.window.destroy()
        elif result == 'tie':
            answer = messagebox.askyesno("Game Over", "It's a tie! Play again?")
            if answer:
                self.reset_game()
            else:
                self.window.destroy()

    def reset_game(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.status_label.config(text="Your Turn (X)")
        for i in range(9):
            self.buttons[i].config(text=' ', state=tk.NORMAL, fg=TEXT_COLOR)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    while True:
        game = TicTacToe()
        game.run()
        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            continue
        else:
            break