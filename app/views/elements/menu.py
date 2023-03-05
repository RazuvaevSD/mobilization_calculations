from tkinter import Button, Frame


class MenuControl(Frame):
    def __init__(self, *args, **kwargs) -> None:
        menu = super().__init__(*args, **kwargs)
        self.pack(side='top', fill='x')
        self.buttons = {}
        return menu

    def add_btn(self,
                id,
                master=None,
                background='steel blue',
                foreground='white',
                activebackground='LightSteelBlue3',
                *args, **kwargs):
        btn = Button(master=master or self,
                     background=background,
                     foreground=foreground,
                     activebackground=activebackground,
                     *args, **kwargs)
        btn.pack(side='left')
        self.buttons[id] = btn

    def get(self, id):
        return self.buttons[id]
