import random
from tkinter import *
from tkinter import messagebox


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Виселица")
        self.root.geometry("1500x1400")

        # Список слов для игры
        self.words = [ "библиотека", "яблоко", "банан", "вишня", "дыня", "ежевика",
    "жираф", "зебра", "индюк", "кенгуру", "лев",
    "малина", "носорог", "орел", "панда", "рис",
    "слон", "тигр", "утка", "фламинго", "хлеб", "правило" ]

        # Настройки игры
        self.max_attempts = 6
        self.attempts_left = self.max_attempts
        self.current_word = ""
        self.guessed_letters = []
        self.hidden_word = []

        # Создание элементов интерфейса
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        # Метка для отображения слова
        self.word_label = Label(self.root, text="", font=("Arial", 24))
        self.word_label.pack(pady=20)

        # Метка для отображения оставшихся попыток
        self.attempts_label = Label(self.root, text=f"Осталось попыток: {self.attempts_left}", font=("Arial", 14))
        self.attempts_label.pack()

        # Метка для отображения использованных букв
        self.used_letters_label = Label(self.root, text="Использованные буквы: ", font=("Arial", 12))
        self.used_letters_label.pack(pady=10)

        # Поле ввода для буквы
        self.letter_entry = Entry(self.root, font=("Arial", 14), width=3)
        self.letter_entry.pack(pady=10)

        # Кнопка для отправки буквы
        self.guess_button = Button(self.root, text="Угадать", command=self.make_guess, font=("Arial", 12))
        self.guess_button.pack()

        # Кнопка для новой игры
        self.new_game_button = Button(self.root, text="Новая игра", command=self.start_new_game, font=("Arial", 12))
        self.new_game_button.pack(pady=10)

        # Холст для рисования виселицы
        self.canvas = Canvas(self.root, width=200, height=200, bg="white")
        self.canvas.pack()

    def start_new_game(self):
        "Начинает новую игру"
        self.current_word = random.choice(self.words).lower()
        self.guessed_letters = []
        self.attempts_left = self.max_attempts
        self.hidden_word = ["_" for _ in self.current_word]

        self.update_display()
        self.draw_gallows()

    def update_display(self):
        "Обновляет отображение игры"
        # Обновляем отображение слова
        display_word = " ".join(self.hidden_word)
        self.word_label.config(text=display_word)

        # Обновляем количество попыток
        self.attempts_label.config(text=f"Осталось попыток: {self.attempts_left}")

        # Обновляем использованные буквы
        used_letters = ", ".join(self.guessed_letters)
        self.used_letters_label.config(text=f"Использованные буквы: {used_letters}")

        # Очищаем поле ввода
        self.letter_entry.delete(0, END)

    def make_guess(self):
        "Обрабатывает попытку угадать букву"
        letter = self.letter_entry.get().lower()

        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите одну букву")
            return

        if letter in self.guessed_letters:
            messagebox.showwarning("Ошибка", "Вы уже пробовали эту букву")
            return

        self.guessed_letters.append(letter)

        if letter in self.current_word:
            # Буква угадана правильно
            for i, char in enumerate(self.current_word):
                if char == letter:
                    self.hidden_word[i] = letter
        else:
            # Буква не угадана
            self.attempts_left -= 1
            self.draw_hangman()

        self.update_display()
        self.check_game_status()

    def check_game_status(self):
        "Проверяет, закончена ли игра"
        if "_" not in self.hidden_word:
            messagebox.showinfo("Поздравляем!", f"Вы выиграли! Слово: {self.current_word}")
            self.start_new_game()
        elif self.attempts_left <= 0:
            messagebox.showinfo("Игра окончена", f"Вы проиграли. Слово было: {self.current_word}")
            self.start_new_game()

    def draw_gallows(self):
        "Рисует виселицу"
        self.canvas.delete("all")
        self.canvas.create_line(50, 180, 150, 180, width=3)  # Основание
        self.canvas.create_line(100, 180, 100, 50, width=3)  # Вертикальная стойка
        self.canvas.create_line(100, 50, 150, 50, width=3)  # Верхняя перекладина
        self.canvas.create_line(150, 50, 150, 70, width=3)  # Веревка

    def draw_hangman(self):
        "Рисует части тела висельника в зависимости от количества ошибок"
        errors = self.max_attempts - self.attempts_left

        if errors == 1:
            self.canvas.create_oval(140, 70, 160, 90, width=3)  # Голова
        if errors == 2:
            self.canvas.create_line(150, 90, 150, 130, width=3)  # Тело
        if errors == 3:
            self.canvas.create_line(150, 100, 130, 110, width=3)  # Левая рука
        if errors == 4:
            self.canvas.create_line(150, 100, 170, 110, width=3)  # Правая рука
        if errors == 5:
            self.canvas.create_line(150, 130, 130, 160, width=3)  # Левая нога
        if errors == 6:
            self.canvas.create_line(150, 130, 170, 160, width=3)  # Правая нога


# Запуск игры
if __name__ == "__main__":
    root = Tk()
    game = HangmanGame(root)
    root.mainloop()