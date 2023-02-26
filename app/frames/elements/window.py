from tkinter import FALSE, Frame, Tk


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
            name='main_frame', bg='white'
        )
        self.main_frame.pack(fill='both', expand=True)