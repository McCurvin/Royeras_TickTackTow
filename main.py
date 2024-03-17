import tkinter as tk
import tkinter.messagebox as messagebox
import os

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.player1_name = ""
        self.player2_name = ""
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.wins = {"Player 1": 0, "Player 2": 0}

        self.create_labels()
        self.create_board()
        self.load_leaderboard()  # Load leaderboard when the game starts

    def create_labels(self):
        tk.Label(self.root, text="Player 1 (X):").grid(row=0, column=0)
        self.player1_entry = tk.Entry(self.root)
        self.player1_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Player 2 (O):").grid(row=1, column=0)
        self.player2_entry = tk.Entry(self.root)
        self.player2_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Start Game", command=self.start_game).grid(row=2, columnspan=2)

        self.leaderboard_label = tk.Label(self.root, text="Leaderboard")
        self.leaderboard_label.grid(row=3, columnspan=2)

        self.update_labels()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=" ", width=10, height=4,
                                   command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i+4, column=j)
                self.buttons.append(button)

    def start_game(self):
        self.player1_name = self.player1_entry.get().strip()
        self.player2_name = self.player2_entry.get().strip()

        if not self.player1_name or not self.player2_name:
            messagebox.showerror("Error", "Please enter both player names.")
            return

        self.reset_board()
        self.update_labels()

    def on_click(self, row, col):
        index = 3 * row + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner() or self.check_draw():
                self.end_game()
            else:
                self.toggle_player()

    def toggle_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_labels()

    def update_labels(self):
        self.leaderboard_label.config(text=f"Leaderboard\n{self.player1_name}: {self.wins.get(self.player1_name, 0)} "
                                            f"| {self.player2_name}: {self.wins.get(self.player2_name, 0)}\nCurrent Turn: {self.current_player}")

    def check_winner(self):
        lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != " ":
                winner = self.player1_name if self.board[line[0]] == "X" else self.player2_name
                self.wins[winner] = self.wins.get(winner, 0) + 1
                self.save_leaderboard()
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.load_leaderboard()  # Reload leaderboard data after a game ends
                self.update_labels()  # Update labels after reloading leaderboard
                return True
        return False

    def check_draw(self):
        if " " not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        return False

    def end_game(self):
        self.update_labels()
        self.save_leaderboard()
        self.load_leaderboard()  # Reload leaderboard data after a game ends

    def reset_board(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")

    def load_leaderboard(self):
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    player, wins = line.strip().split(":")
                    self.wins[player] = int(wins)
            self.update_labels()  # Update the leaderboard labels after loading

    def save_leaderboard(self):
        with open("leaderboard.txt", "w") as file:
            for player, wins in self.wins.items():
                file.write(f"{player}:{wins}\n")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()