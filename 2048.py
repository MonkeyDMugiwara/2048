import random
import tkinter as tk
from tkinter import messagebox
import time

class Game2048:
    def __init__(self, root):
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title("2048")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#faf8ef")

        # Couleurs des cases selon la valeur
        self.colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#3c3a32"
        }

        # Couleurs du texte selon la valeur
        self.text_colors = {
            0: "#cdc1b4",
            2: "#776e65",
            4: "#776e65",
            8: "#f9f6f2",
            16: "#f9f6f2",
            32: "#f9f6f2",
            64: "#f9f6f2",
            128: "#f9f6f2",
            256: "#f9f6f2",
            512: "#f9f6f2",
            1024: "#f9f6f2",
            2048: "#f9f6f2",
            4096: "#f9f6f2",
            8192: "#f9f6f2"
        }

        # Initialisation des variables
        self.score = 0
        self.best_score = 0
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.game_over = False
        self.win = False
        self.can_continue = False

        # Création des éléments GUI
        self.create_widgets()

        # Liaison des touches fléchées
        self.root.bind("<Left>", lambda event: self.move("left"))
        self.root.bind("<Right>", lambda event: self.move("right"))
        self.root.bind("<Up>", lambda event: self.move("up"))
        self.root.bind("<Down>", lambda event: self.move("down"))

        # Démarrer une nouvelle partie
        self.new_game()

    def create_widgets(self):
        # Création de l'en-tête
        header_frame = tk.Frame(self.root, bg="#faf8ef")
        header_frame.pack(pady=10, fill="x")

        # Titre
        title_label = tk.Label(header_frame, text="2048", font=("Arial", 48, "bold"), fg="#776e65", bg="#faf8ef")
        title_label.pack(side="left", padx=10)

        # Conteneur pour les scores
        score_frames_container = tk.Frame(header_frame, bg="#faf8ef")
        score_frames_container.pack(side="right", padx=10)

        # Score actuel
        score_frame = tk.Frame(score_frames_container, bg="#bbada0", bd=0, relief="solid", padx=10, pady=5)
        score_frame.pack(side="left", padx=5)

        tk.Label(score_frame, text="SCORE", font=("Arial", 12), fg="#eee4da", bg="#bbada0").pack()
        self.score_label = tk.Label(score_frame, text="0", font=("Arial", 16, "bold"), fg="white", bg="#bbada0")
        self.score_label.pack()

        # Meilleur score
        best_score_frame = tk.Frame(score_frames_container, bg="#bbada0", bd=0, relief="solid", padx=10, pady=5)
        best_score_frame.pack(side="left", padx=5)

        tk.Label(best_score_frame, text="BEST", font=("Arial", 12), fg="#eee4da", bg="#bbada0").pack()
        self.best_score_label = tk.Label(best_score_frame, text="0", font=("Arial", 16, "bold"), fg="white", bg="#bbada0")
        self.best_score_label.pack()

        # Bouton nouvelle partie
        button_frame = tk.Frame(self.root, bg="#faf8ef")
        button_frame.pack(pady=5)

        new_game_btn = tk.Button(button_frame, text="New Game", font=("Arial", 12, "bold"), 
                               bg="#8f7a66", fg="white", relief="flat", 
                               command=self.new_game, padx=10, pady=5)
        new_game_btn.pack()

        # Création de la grille
        self.grid_frame = tk.Frame(self.root, bg="#bbada0", padx=10, pady=10)
        self.grid_frame.pack(pady=5)

        # Création des cellules
        self.cell_frames = []
        cell_size = 75
        for i in range(4):
            row_frames = []
            for j in range(4):
                cell_frame = tk.Frame(self.grid_frame, width=cell_size, height=cell_size, bg="#cdc1b4")
                cell_frame.grid(row=i, column=j, padx=4, pady=4)
                cell_frame.grid_propagate(False)

                cell_label = tk.Label(cell_frame, text="", font=("Arial", 24, "bold"), 
                                    bg="#cdc1b4", fg="#776e65")
                cell_label.place(relx=0.5, rely=0.5, anchor="center")

                row_frames.append(cell_label)
            self.cell_frames.append(row_frames)

        # Instructions
        instructions = "Utilisez les flèches pour déplacer les tuiles."
        instruction_label = tk.Label(self.root, text=instructions, font=("Arial", 10),
                                  fg="#776e65", bg="#faf8ef", justify="left")
        instruction_label.pack(pady=5)

    def new_game(self):
        # Réinitialisation des variables
        self.score = 0
        self.update_score()
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.game_over = False
        self.win = False
        self.can_continue = False

        # Ajoute deux tuiles
        self.add_new_tile()
        self.add_new_tile()

        # Mise à jour de l'affichage
        self.update_grid_display()

    def add_new_tile(self):
        # Cherche les cases vides
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            return True
        return False

    def update_grid_display(self):
        # Mise à jour visuelle de la grille
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                cell = self.cell_frames[i][j]

                cell.config(text="" if value == 0 else str(value))

                bg_color = self.colors.get(value, "#3c3a32")
                text_color = self.text_colors.get(value, "#f9f6f2")
                cell.config(bg=bg_color, fg=text_color)
                cell.master.config(bg=bg_color)

                if value == 0:
                    font_size = 24
                elif value < 100:
                    font_size = 24
                elif value < 1000:
                    font_size = 20
                else:
                    font_size = 16

                cell.config(font=("Arial", font_size, "bold"))

    def update_score(self):
        # Met à jour le score
        self.score_label.config(text=str(self.score))
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_score_label.config(text=str(self.best_score))

    def transpose(self):
        # Transpose la grille
        self.grid = [[self.grid[j][i] for j in range(4)] for i in range(4)]

    def reverse(self):
        # Inverse chaque ligne
        for i in range(4):
            self.grid[i].reverse()

    def compress(self):
        # Compresse la grille à gauche
        changed = False
        new_grid = [[0 for _ in range(4)] for _ in range(4)]

        for i in range(4):
            pos = 0
            for j in range(4):
                if self.grid[i][j] != 0:
                    new_grid[i][pos] = self.grid[i][j]
                    if j != pos:
                        changed = True
                    pos += 1

        self.grid = new_grid
        return changed

    def merge(self):
        # Fusionne les tuiles identiques
        changed = False
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] != 0 and self.grid[i][j] == self.grid[i][j + 1]:
                    self.grid[i][j] *= 2
                    self.grid[i][j + 1] = 0
                    self.score += self.grid[i][j]
                    changed = True

                    if self.grid[i][j] == 2048 and not self.can_continue:
                        self.win = True

        return changed

    def can_move(self):
        # Vérifie si un déplacement est possible
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True

        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return True

        for j in range(4):
            for i in range(3):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return True

        return False

    def move(self, direction):
        if self.game_over:
            return

        if direction == "left":
            changed = self.move_left()
        elif direction == "right":
            self.reverse()
            changed = self.move_left()
            self.reverse()
        elif direction == "up":
            self.transpose()
            changed = self.move_left()
            self.transpose()
        elif direction == "down":
            self.transpose()
            self.reverse()
            changed = self.move_left()
            self.reverse()
            self.transpose()

        self.update_score()
        self.update_grid_display()

        if self.win and not self.can_continue:
            self.handle_win()

        if not self.can_move():
            self.game_over = True
            self.handle_game_over()

    def move_left(self):
        changed1 = self.compress()
        changed2 = self.merge()
        changed3 = self.compress()

        if changed1 or changed2 or changed3:
            self.add_new_tile()

        return changed1 or changed2 or changed3

    def handle_win(self):
        # Gère la victoire
        response = messagebox.askyesno("Félicitations!", 
                                       "Vous avez atteint 2048 ! Voulez-vous continuer à jouer?")
        if response:
            self.can_continue = True
        else:
            self.game_over = True
            messagebox.showinfo("Jeu terminé", f"Félicitations ! Votre score final est : {self.score}")
            self.new_game()

    def handle_game_over(self):
        # Gère la fin de partie
        messagebox.showinfo("Jeu terminé", f"Partie terminée ! Votre score final est : {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
