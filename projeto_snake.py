import customtkinter as ctk
import random
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

RANKING_FILE = "nomes.txt"

def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_ranking(ranking):
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=4)

def get_top3(ranking):
    return sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:3]

class UsernameScreen(ctk.CTkFrame):
    def __init__(self, master, start_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.start_callback = start_callback
        self.pack(padx=20, pady=20)

        ctk.CTkLabel(self, text="🐍 Bem-vindo ao Snake!", font=("Arial", 24, "bold")).pack(pady=(10, 20))

        ctk.CTkLabel(self, text="Digite seu nome de usuário:", font=("Arial", 16)).pack(pady=5)

        self.username_entry = ctk.CTkEntry(self, width=250, height=35, placeholder_text="Ex: Gustavo")
        self.username_entry.pack(pady=10)
        self.username_entry.focus()

        ctk.CTkButton(self, text="🎮 Iniciar Jogo", width=200, height=40, command=self.on_start).pack(pady=15)

        ranking = carregar_ranking()
        top3 = get_top3(ranking)
        ranking_text = "🏆 Ranking TOP 3:\n"
        for i, (user, score) in enumerate(top3, 1):
            ranking_text += f"{i}º - {user}: {score}\n"
        if not top3:
            ranking_text += "Nenhum registro ainda."

        ranking_frame = ctk.CTkFrame(self, corner_radius=10)
        ranking_frame.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(ranking_frame, text=ranking_text, font=("Arial", 13)).pack(padx=10, pady=10)

    def on_start(self):
        username = self.username_entry.get().strip()
        if username:
            self.start_callback(username)

class SnakeGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Jogo Snake - Jogador: {self.username}")
        
        self.canvas = ctk.CTkCanvas(root, width=400, height=400, bg="black")
        self.canvas.pack(pady=20)

        self.grid_size = 20
        self.cell_size = 20
        self.snake = [(100, 100)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.score = 0
        self.game_over = False

        self.score_label = ctk.CTkLabel(root, text=f"Pontuação: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        self.draw_snake()
        self.draw_food()
        self.root.bind("<KeyPress>", self.change_direction)
        self.move()

    def spawn_food(self):
        x = random.randrange(0, 400, self.cell_size)
        y = random.randrange(0, 400, self.cell_size)
        return (x, y)

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_oval(x, y, x + self.cell_size, y + self.cell_size,
                                    fill="lime", tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                     fill="red", tags="food")

    def change_direction(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def move(self):
        if self.game_over:
            return

        x, y = self.snake[0]
        if self.direction == "Up":
            y -= self.cell_size
        elif self.direction == "Down":
            y += self.cell_size
        elif self.direction == "Left":
            x -= self.cell_size
        elif self.direction == "Right":
            x += self.cell_size

        new_head = (x, y)
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.configure(text=f"Pontuação: {self.score}")
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        if (x < 0 or x >= 400 or y < 0 or y >= 400 or new_head in self.snake[1:]):
            self.game_over = True
            self.canvas.create_text(200, 200, text="💀 Game Over 💀", fill="white", font=("Arial", 24, "bold"))
            self.atualizar_ranking()
            self.mostrar_reiniciar()
            return

        self.draw_snake()
        self.draw_food()
        self.root.after(100, self.move)

    def atualizar_ranking(self):
        ranking = carregar_ranking()
        if self.username not in ranking or self.score > ranking[self.username]:
            ranking[self.username] = self.score
            salvar_ranking(ranking)

    def mostrar_reiniciar(self):
        def reiniciar():
            self.canvas.destroy()
            self.score_label.destroy()
            UsernameScreen(self.root, start_game)

        ctk.CTkButton(self.root, text="🔁 Jogar Novamente", width=200, height=35, command=reiniciar).pack(pady=10)

def start_game(username):
    for widget in root.winfo_children():
        widget.destroy()
    SnakeGame(root, username)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("500x600")
    root.eval("tk::PlaceWindow . center") 
    UsernameScreen(root, start_game)
    root.mainloop()


#====================================================fontes====================================================#

#Fonte que usei para randomizar as posicoes das frutas: https://docs.python.org/pt-br/3.13/library/random.html
#Demorei um pouco pra achar isso, mas os movimentos usando as setas eu meio que usei daqui: https://stackoverflow.com/questions/19264066/tracing-keypresses-in-python
#Ha alguns repositorios na internet semelhantes, mas a diferenca e que eu fiz usando customtkinter, que e uma biblioteca que deixa o tkinter mais bonito e moderno.
#o import OS serve para verificar se o arquivo de ranking existe, e se nao existir, ele cria um novo arquivo vazio.
#o import JSON serve para salvar o ranking em um arquivo, e carregar o ranking quando o jogo inicia.
#A ideia que eu tive veio desse video: https://www.youtube.com/watch?v=FtqWCo1_I4g
#====================================================bla bla bla bla===============================================#

#Quem quiser ver isso, meu projeto esta no meu github: https://github.com/junxhook
#Como eu nao sou perfeito, logicamente eu usei IA, mas eu fiz o maximo possivel para que o codigo fosse meu, e nao de outra pessoa.
#Espero que tenham gostado do projeto, e que ele possa ser usado para aprender mais sobre python e ctk.
#Se tiverem alguma duvida, podem me chamar no discord: 3ykk