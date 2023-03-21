import tkinter as tk
import time
import tkinter.messagebox as mb
from multiprocessing import Value


Arial_11 = ("Arial", 11)
users_list = {'root':'123'}
attempt_counter = 0
def error_message(error):
    mb.showerror("Ошибка", error)

class App(tk.Tk):
    def __init__(self,tumb_for_sound, tumb_for_disc, tumb_for_blur,tumb_for_file):
        super().__init__()
        self.tumb_for_sound=tumb_for_sound
        self.tumb_for_disc=tumb_for_disc
        self.tumb_for_blur=tumb_for_blur
        self.tumb_for_file=tumb_for_file

        self.geometry('250x140-1670+907')     # Установка размера окна
        self.title("Авторизация")     # Название окна
        self.resizable(width=False, height=False)   # Запрещаем менять размер окна

        user_label = tk.Label(self, text="user", font=Arial_11, width=25)    # Текст "user"
        user_label.grid(row=0, column=0, sticky="S", padx=10)
        user_entry = tk.Entry(self, width=25)     # Поле для ввода user
        user_entry.grid(row=1, column=0, sticky="N", padx=10)

        pwd_label = tk.Label(self, text="password", font=Arial_11, width=25)     # Текст "password"
        pwd_label.grid(row=2, column=0, sticky="S", padx=10)
        pwd_entry = tk.Entry(self, width=25, show='*')     # Поле для ввода password
        pwd_entry.grid(row=3, column=0, sticky="N", padx=10)

        '''
        В параметр command для кнопки можно запихать лямбда функцию, чтобы использовать эту функцию с параметрами.
        Таким образом происходит передача заполненных пользователем данных
        '''

        connect_button = tk.Button(self, text="Войти", font=Arial_11, width=10,
                                   command=lambda: self.enter_button(connect_button, user_entry.get(), pwd_entry.get()))
        connect_button.grid(row=4, column=0, pady=10, padx=10)


    def enter_button(self, connect_button, user, password):    # Что происходит при нажатии на кнопку
        global attempt_counter
        if (user in users_list and password == users_list[user]):    # Если пользователь есть в нашем словаре
            Config_window(self,self.tumb_for_sound, self.tumb_for_disc, self.tumb_for_blur,self.tumb_for_file)     # Открываем новое окно
        else:
            attempt_counter += 1    # Инкрементируем счетчик попыток входа
            if (attempt_counter > 3):   # Если неудачных попыток больше трех
                error_message("Слишком большое количество неудачных попыток входа")
                attempt_counter = 0     # Сбрасываем счетчик
                connect_button['state'] = 'disabled'    # Выключаем кнопку
                time.sleep(10)     # Ждем 10 секунд
                connect_button['state'] = 'active'     # Включаем кнопку
            else:
                error_message("У вас нет прав для настройки программы")     # Выводим сообщение о неправильном вводе юзера

class Config_window(tk.Toplevel):
    def __init__(self, parent_window,tumb_for_sound, tumb_for_disc, tumb_for_blur,tumb_for_file):
        parent_window.withdraw()
        tk.Toplevel.__init__(self, parent_window)      # Инициализация окна
        self.title("Config")  # Название окна
        self.geometry('300x220-1600+800') 
        self.protocol("WM_DELETE_WINDOW",
                               lambda: parent_window.destroy())  # Уничтожение main окна при выключении окна настроек
        self.resizable(width=False, height=False)
        container = tk.Frame(self)
        container.pack(fill="both", expand="yes")

        self.frames = {}        # Создаем словарь с фреймами
        frame = Tumbler_page(container, self,tumb_for_sound, tumb_for_disc, tumb_for_blur)# Закидываем в него два фрейма разных классов
        self.frames[Tumbler_page] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame = Dictionary_page(container, self,tumb_for_file)
        self.frames[Dictionary_page] = frame
        frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(Dictionary_page)     #  Показываем страницу со словарем

    def show_frame(self, cont):     # Функция переключения фрейма
        frame = self.frames[cont]
        frame.tkraise()

class Dictionary_page(tk.Frame):
    def __init__(self, parent, controller,tumb_for_file):
        self.tumb_for_file=tumb_for_file
        tk.Frame.__init__(self, parent)
        mode_panel = tk.Frame(self)    # Фрейм с кнопками переключения режима
        mode_panel.grid(row=0, column=0, sticky="ew", columnspan=3)  # Фрейм для кнопок переключения страниц

        to_dictionary = tk.Button(mode_panel, text="К словарю", font=('Arial', 10), width=11, state="disabled", relief="sunken")
        to_dictionary.grid(row=0, column=0)     # Кнопка "К словарю" неактивна

        to_config = tk.Button(mode_panel, text="К настройкам", font=('Arial', 10),   # Кнопка "к настройкам" переключает страницу
                              command=lambda: controller.show_frame(Tumbler_page))
        to_config.grid(row=0, column=2)

        words_listbox = tk.Listbox(self)  # Размещение листбокса для слов в гриде
        words_listbox.grid(row=1, column=0, columnspan=3, sticky="news")

        file_name = "banned words.txt"      # Название файла с запрещенными словами

        with open(file_name, "r", encoding="utf-8") as file:     # открываем файл
            for word in file:
                words_listbox.insert("end", word)       # Запихиваем каждое слово в листбокс

        scrollbar = tk.Scrollbar(self)  # Размещение скроллбара в гриде
        scrollbar.grid(row=1, column=3, sticky="nws")

        words_listbox.config(yscrollcommand=scrollbar.set)  # Прикрепление скроллбара к листбоксу
        scrollbar.config(command=words_listbox.yview)

        word_entry = tk.Entry(self, width=25)
        word_entry.grid(row=2, column=0, sticky="w")

        entry_button = tk.Button(self, text="Добавить", font=('Arial', 10),
                                 command=lambda: self.add_to_dictionary(words_listbox, word_entry.get(), file_name))
        entry_button.grid(row=2, column=1, sticky="e")

        delete_button = tk.Button(self, text="Удалить", font=('Arial', 10),
                                 command=lambda: self.delete_from_dictionary(words_listbox, file_name))
        delete_button.grid(row=2, column=2, sticky="e")

    def add_to_dictionary(self, words_listbox, word, file_name):
        if (not word):
            error_message("Введите слово для добавления")
        elif (word.strip(" ") + '\n' in words_listbox.get(0, words_listbox.size() - 1)):  # Проверка на наличие слова в листбоксе
            error_message("Такое слово уже есть в словаре")
        else:
            words_listbox.insert("end", word + '\n')
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(word + "\n")
            self.tumb_for_file.value=1

    def delete_from_dictionary(self, words_listbox, file_name):
        if (words_listbox.curselection()):
            deleted_word = words_listbox.get(words_listbox.curselection())         # Слово для удаления
            words_listbox.delete(words_listbox.curselection())
            with open(file_name, "r", encoding="utf-8") as file:
                lines = file.readlines()
            with open(file_name, "w", encoding="utf-8") as file:
                for line in lines:
                    check_line = line
                    if line != deleted_word:
                        file.write(line)
            self.tumb_for_file.value=1
        else:
            error_message("Выберите элемент из списка")


class Tumbler_page(tk.Frame):

    def __init__(self, parent, controller,tumb_for_sound, tumb_for_disc, tumb_for_blur):
        tk.Frame.__init__(self, parent)
        self.tumb_for_sound=tumb_for_sound
        self.tumb_for_disc=tumb_for_disc
        self.tumb_for_blur=tumb_for_blur
        self.sb=tk.IntVar()
        self.ds=tk.IntVar()
        self.bl=tk.IntVar()

        to_dictionary = tk.Button(self, text="К словарю", font=('Arial', 10), width=11,  # Кнопка "к словарю" переключает страницу
                                  command=lambda: controller.show_frame(Dictionary_page))
        to_dictionary.grid(row=0, column=0)

        to_config = tk.Button(self, text="К настройкам", font=('Arial', 10), state="disabled", relief="sunken")
        to_config.grid(row=0, column=1)     # Кнопка "К настройкам" неактивна

        disclaimer_button = tk.Checkbutton(self, text="Отображение дисклеймера",variable=self.ds, command=self.disc)
        disclaimer_button.grid(row=1, column=0, columnspan=2, sticky="w", pady=10)

        blur_button = tk.Checkbutton(self, text="Замыливание текста",variable=self.bl, command=self.blur)
        blur_button.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)

        sound_button = tk.Checkbutton(self, text="Звук",variable=self.sb, command=self.sound)
        sound_button.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)
    
    def disc(self):
        self.tumb_for_disc.value=self.ds.get()
    def blur(self):
        self.tumb_for_blur.value=self.bl.get()
    def sound(self):
        self.tumb_for_sound.value=self.sb.get()

def main():
    autorization_window = App()
    autorization_window.mainloop()

if __name__ == "__main__":
    main()