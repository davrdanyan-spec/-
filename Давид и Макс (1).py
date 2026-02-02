import time
import customtkinter as ctk
from PIL import ImageTk, Image
from tkinter import messagebox

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class StartWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Введите имя")
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Введите имя Тамагочи")
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Старт", command=self.start)
        self.button.pack(pady=20)

    def start(self):
        name = self.entry.get().strip()
        if not name:
            self.label.configure(text="Введите имя!")
            return

        self.destroy()
        TamagotchiApp(name).mainloop()


class TamagotchiApp(ctk.CTk):
    def __init__(self, name):
        super().__init__()
        self.title("Zavid and Zmax")
        self.geometry("420x540")

        ctk.CTkLabel(self, text=f"Привет, {name}!", font=("Arial", 18)).pack(pady=10)


        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.cleanliness = 50
        self.alive = True


        img = Image.open("User-Avatar-Free-PNG-Image.png")
        img = img.resize((350, 350))
        self.photo = ImageTk.PhotoImage(img)

        canvas = ctk.CTkCanvas(self, width=350, height=350, highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=self.photo)


        self.hunger_bar = self.make_bar("Голод")
        self.clean_bar = self.make_bar("Чистота")
        self.happy_bar = self.make_bar("Счастье")
        self.energy_bar = self.make_bar("Энергия")


        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        ctk.CTkButton(frame, text="Кормить", command=self.feed).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame, text="Играть", command=self.play).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame, text="Спать", command=self.sleep).grid(row=0, column=2, padx=5)
        ctk.CTkButton(self, text="Чистить", command=self.clean).pack(pady=5)

        self.update_ui()
        self.after(1500, self.game_loop)

    def make_bar(self, text):
        ctk.CTkLabel(self, text=text).pack()
        bar = ctk.CTkProgressBar(self, width=320)
        bar.pack(pady=5)
        return bar

    def update_ui(self):
        self.hunger_bar.set(self.hunger / 100)
        self.clean_bar.set(self.cleanliness / 100)
        self.happy_bar.set(self.happiness / 100)
        self.energy_bar.set(self.energy / 100)


    def feed(self):
        self.hunger = max(0, self.hunger - 15)
        self.happiness = min(100, self.happiness + 5)
        self.update_ui()

    def play(self):
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy - 10)
        self.hunger = min(100, self.hunger + 5)
        self.update_ui()

    def sleep(self):
        self.energy = min(100, self.energy + 20)
        self.hunger = min(100, self.hunger + 5)
        self.update_ui()

    def clean(self):
        self.cleanliness = min(100, self.cleanliness + 20)
        self.update_ui()

    def game_loop(self):
        if not self.alive:
            return

        self.hunger = min(100, self.hunger + 2)
        self.cleanliness = max(0, self.cleanliness - 2)
        self.energy = max(0, self.energy - 1)
        self.happiness = max(0, self.happiness - 1)

        self.update_ui()

        if self.hunger >= 100:
            self.game_over("погиб от голода")
        elif self.energy <= 0:
            self.game_over("умер от усталости")
        elif self.happiness <= 0:
            self.game_over("впал в депрессию")

        self.after(1500, self.game_loop)

    def game_over(self, reason):
        self.alive = False
        messagebox.showinfo("Игра окончена", f"Ваш Тамагочи {reason}.")


if __name__ == "__main__":
    StartWindow().mainloop()

