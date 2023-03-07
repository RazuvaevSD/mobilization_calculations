from tkinter import Button, Scrollbar, Text, Toplevel


class Protocol(Toplevel):
    def __init__(self, title, geometry, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.geometry(geometry)

        self.message = Text(master=self, background='white', wrap='word')
        self.message.pack(fill='both', expand=True)
        self.message.insert('end', message)

        vert_scroll = Scrollbar(master=self.message,
                                command=self.message.yview)
        vert_scroll.pack(side='right', fill='y')
        self.message.config(yscrollcommand=vert_scroll.set)

        self.btn = Button(master=self, background='white', text='OK',
                          command=self.exit_btn)
        self.btn.pack(side='bottom')

    def exit_btn(self):
        self.destroy()
        self.update()
