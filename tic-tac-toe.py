import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master, mode, mode2):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.buttons = []
        self.mode = mode
        self.mode2 = mode2
        self.create_board()
    
    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text='', font=('Arial', 20), width=8, height=4,
                                   command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
        
        if (self.mode == 'ai' and self.current_player == 'X') or (self.mode2 == 'ai' and self.current_player == 'O'):
            self.ai_move()
    
    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.update_gui(row, col)
            print("Player", self.current_player, "moved to position:", index)
            print("Current Board State:")
            self.print_board()
            if self.check_winner() or self.is_board_full():
                self.game_over()
            else:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                if (self.mode == 'ai' and self.current_player == 'X') or (self.mode2 == 'ai' and self.current_player == 'O'):
                    self.ai_move()
        else:
            messagebox.showerror("Invalid Move", "That space is already taken!")

    def update_gui(self, row, col):
        index = row * 3 + col
        if self.current_player == 'X':
            self.buttons[index].config(text=self.current_player, state='disabled', bg='#00FF00', fg='white')
        else:
            self.buttons[index].config(text=self.current_player, state='disabled', bg='#3FBFFF', fg='white')

    def print_board(self):
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            if i < 6:
                print("---------")

    def check_winner(self):
        win_patterns = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                        [0, 3, 6], [1, 4, 7], [2, 5, 8],
                        [0, 4, 8], [2, 4, 6]]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != ' ':
                return True
        return False

    def is_board_full(self):
        return ' ' not in self.board

    def game_over(self):
        if self.check_winner():
            winner = "Player " + self.current_player + " wins!"
            messagebox.showinfo("Game Over", winner)
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a tie!")
        self.reset_board()

    def reset_board(self):
        for i in range(9):
            self.board[i] = ' '
            self.buttons[i].config(text='', state='normal', bg='SystemButtonFace', fg='black')
        self.current_player = 'X'
        if self.mode == 'ai' and self.mode2 == 'ai':
            self.ai_move()

    def ai_move(self):
        if self.current_player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.current_player
                score = self.minimax(self.board, 0, False, opponent)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        self.make_move(best_move // 3, best_move % 3)

    def minimax(self, board, depth, is_maximizing, opponent):
        if self.check_winner():
            if is_maximizing:
                return -10 + depth
            else:
                return 10 - depth
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.current_player
                    score = self.minimax(board, depth + 1, False, opponent)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = opponent
                    score = self.minimax(board, depth + 1, True, opponent)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

def start_game():
    global mode, mode2, mode_var, mode_var2
    mode = mode_var.get()
    mode2 = mode_var2.get()
    root = tk.Tk()
    game = TicTacToe(root, mode, mode2)
    root.mainloop()


root = tk.Tk()
root.title("Tic Tac Toe")

mode_var = tk.StringVar(value="human")  
mode_var2 = tk.StringVar(value="human") 

tk.Label(root, text="Select Mode for Player 1 (X):").pack()
tk.Radiobutton(root, text="Human", variable=mode_var, value="human").pack()
tk.Radiobutton(root, text="AI", variable=mode_var, value="ai").pack()
tk.Label(root, text="Select Mode for Player 2 (O):").pack()
tk.Radiobutton(root, text="Human", variable=mode_var2, value="human").pack()
tk.Radiobutton(root, text="AI", variable=mode_var2, value="ai").pack()


start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()
start_button.configure(bg='#00FF00')

root.mainloop()
