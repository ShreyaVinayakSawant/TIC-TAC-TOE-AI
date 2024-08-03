import tkinter as tk
from tkinter import messagebox

def check_win(board, player):
    for row in range(3):
        if all([cell == player for cell in board[row]]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    return all([cell != '' for row in board for cell in row])

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']

def make_move(board, move, player):
    board[move[0]][move[1]] = player

def undo_move(board, move):
    board[move[0]][move[1]] = ''

def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'):
        return 10 - depth
    if check_win(board, 'O'):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for move in get_available_moves(board):
            make_move(board, move, 'X')
            score = minimax(board, depth + 1, False)
            undo_move(board, move)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            make_move(board, move, 'O')
            score = minimax(board, depth + 1, True)
            undo_move(board, move)
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = None
    for possible_move in get_available_moves(board):
        make_move(board, possible_move, 'X')
        score = minimax(board, 0, False)
        undo_move(board, possible_move)
        if score > best_score:
            best_score = score
            move = possible_move
    return move

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        self.create_widgets()

    def create_widgets(self):
        # Frame for the board
        frame = tk.Frame(self.root, bg='lightgray')
        frame.pack(padx=10, pady=10)

        # Create a grid of buttons with custom styles
        for r in range(3):
            for c in range(3):
                button = tk.Button(frame, text='', font=('Arial', 24), width=5, height=2,
                                   bg='white', fg='black', relief='raised',
                                   command=lambda row=r, col=c: self.on_button_click(row, col))
                button.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = button

        # Status Label
        self.status_label = tk.Label(self.root, text="Your turn (O)", font=('Arial', 16), bg='lightgray')
        self.status_label.pack(pady=10)

    def on_button_click(self, row, col):
        if self.board[row][col] != '':
            return
        self.make_move(row, col, 'O')
        if check_win(self.board, 'O'):
            self.show_message("You win!")
            return
        if is_board_full(self.board):
            self.show_message("It's a draw!")
            return

        # AI move
        ai_move = best_move(self.board)
        if ai_move:
            self.make_move(ai_move[0], ai_move[1], 'X')
            if check_win(self.board, 'X'):
                self.show_message("AI wins!")
                return
            if is_board_full(self.board):
                self.show_message("It's a draw!")
                return

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, bg='lightblue' if player == 'X' else 'lightgreen')

    def show_message(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
