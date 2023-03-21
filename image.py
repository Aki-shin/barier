import tkinter as tk
import pygame
from multiprocessing import Value


# функция вывода дисклеймера, получает на вход список категорий деструктивного воздействия
def disclaimer(categories,tumb_for_sound, tumb_for_disc):
    # Создаем функцию для закрытия окна
    def close_window():
        root.destroy()

    # Проигрывание звука
    def play_sound():
        pygame.mixer.music.load("pig.mp3")
        pygame.mixer.music.play()

    if tumb_for_sound.value:
        pygame.init()
        play_sound()

    if tumb_for_disc.value:
        # Создаем главное окно
        root = tk.Tk()
        root.after(5000, root.destroy)
        # Устанавливаем заголовок окна
        root.title("Мое окно")

        # Отключаем стандартную верхнюю панель окна
        root.overrideredirect(True)

        # Устанавливаем цвет фона окна
        root.configure(bg="black")

        # Создаем надпись
        label = tk.Label(root, text="Внимание!", fg="red", bg="black", font=("Arial", 40), pady=10)

        # Размещаем надпись в окне
        label.pack()

        # Создаем надпись
        label2 = tk.Label(root, text="На экране обнаружен контент,\nотносящийся к категории(-ям):",
                        fg="white", bg="black", font=("Arial", 24), pady=20)

        # Размещаем надпись в окне
        label2.pack()

        text = ""
        for category in categories:
            text += f"{category},\n"

        label3 = tk.Label(root, text=text[:-2],
                        fg="red", bg="black", font=("Arial", 24, "italic"), pady=0)

        # Размещаем надпись в окне
        label3.pack()

        label3_height = label3.winfo_reqheight()

        # Создаем кнопку
        button = tk.Button(root, text="Я осознаю потенциальную\nопасность материала", command=close_window,
                        fg="red", font=("Arial", 12))

        # Размещаем кнопку внизу окна
        button.pack(side=tk.BOTTOM, pady=10)

        # Определяем функции для эффектов при наведении курсора на кнопку
        def on_enter(event):
            button.config(bg="gray", fg="white", relief="groove")

        def on_leave(event):
            button.config(bg="white", fg="red", relief="flat")

        # Связываем функции с событиями
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        # Получаем размеры экрана
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Вычисляем координаты центра экрана
        x = (screen_width ) - (500)
        y = (screen_height) - (270)

        # Устанавливаем позицию окна в центре экрана
        root.geometry("500x{}+{}+{}".format(280 + label3_height, x, y - (label3_height)))

        # Делаем окно всегда поверх других окон
        root.wm_attributes("-topmost", 1)

        # Запускаем главный цикл обработки событий
        root.mainloop()
