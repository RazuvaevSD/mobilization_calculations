from tkinter import FALSE, Frame, Tk

from .menu import MenuControl
from .tabs import TabControl


class Window(Tk):

    def __init__(self, *args, **kwargs):
        # Инициализация окна
        self.main = Tk.__init__(self, *args, **kwargs)
        # Глобально отключаем функцию перетаскивания меню
        self.option_add("*tearOff", FALSE)
        # Добавляем Frame
        # как базовый контейнер для остальных элементов управления
        self.main_frame = Frame(
            master=self,
            name='main_frame', bg='steel blue', padx=1, pady=1
        )
        self.main_frame.pack(fill='both', expand=True)
        # Основной контейнер меню (переопределенный Frane)
        self.main_menu = MenuControl(master=self.main_frame,
                                     bg='steel blue',
                                     padx=2, pady=2)
        # Контроллер для табов (переопределенный Notebook)
        self.tab_control = TabControl(master=self.main_frame)
