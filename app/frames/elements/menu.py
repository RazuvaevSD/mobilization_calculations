from tkinter import LEFT, Button, Frame, Menu


class MainMenu(Menu):
    def __init__(self, bg='white', *args, **kwargs):
        super().__init__(bg=bg, *args, **kwargs)


class TabMenu(Frame):
    def __init__(self, bg='white', *args, **kwargs):
        super().__init__(bg=bg, *args, **kwargs)
        self.pack(fill='x', side='top')

    def add_btn(self, bg='white', *args, **kwargs):
        btn = Button(master=self, bg=bg, *args, **kwargs)
        # TODO НАДО ОПРЕДЕЛИТЬ ОТРИСОВКУ В РЯД
        btn.pack(side=LEFT, padx=3, pady=3)
