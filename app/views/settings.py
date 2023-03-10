from tkinter import Button, Entry, Frame, Label, StringVar, Toplevel

from app.services.db.settings import Settings as SettingsDB


class Setting(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Настройки')
        self.geometry('600x300')

        self.org_name = StringVar()
        self.pos_head = StringVar()
        self.pos_coordinator = StringVar()

        self.mainframe = Frame(master=self, background='white')
        self.mainframe.pack(fill='both', ipadx=5, ipady=5, expand=True)

        self.create_fields_frame()
        self.load_settings()

        # кнопки
        self.btn = Button(master=self.mainframe, background='white',
                          borderwidth=0,
                          text='Сохранить', command=self.save)
        self.btn.pack(side='right', anchor='se', padx=3)
        self.btn = Button(master=self.mainframe, background='white',
                          borderwidth=0,
                          text='Отмена', command=self.cancel)
        self.btn.pack(side='right', anchor='se', padx=3)

    def create_fields_frame(self):
        # поля
        frame = Frame(master=self.mainframe, background='white')
        frame.pack(side='top', fill='x', ipadx=3, ipady=3)
        for c in range(20):
            frame.columnconfigure(index=c, weight=1)
        for r in range(10):
            frame.rowconfigure(index=r, weight=1)

        lbl_org_name = Label(master=frame, background='white',
                             text='Наименование организации (дательный падеж)')
        lbl_org_name.grid(row=0, column=0, padx=3, pady=1, sticky='w')
        txt_org_name = Entry(master=frame, background='white',
                             width=100, textvariable=self.org_name)
        txt_org_name.grid(row=1, column=0, columnspan=3,
                          padx=3, pady=1, sticky='w')

        lbl_pos_head = Label(master=frame, background='white',
                             text='Должность руководителя')
        lbl_pos_head.grid(row=2, column=0, padx=3, pady=1, sticky='w')
        txt_pos_head = Entry(master=frame, background='white',
                             width=100, textvariable=self.pos_head)
        txt_pos_head.grid(row=3, column=0, columnspan=3,
                          padx=3, pady=1, sticky='w')

        lbl_pos_coordinator = Label(master=frame, background='white',
                                    text='Должность согласующего')
        lbl_pos_coordinator.grid(row=4, column=0, padx=3, pady=1, sticky='w')
        txt_pos_coordinator = Entry(master=frame, background='white',
                                    width=100,
                                    textvariable=self.pos_coordinator)
        txt_pos_coordinator.grid(row=5, column=0, columnspan=3,
                                 padx=3, pady=1, sticky='w')

    def load_settings(self):
        data = SettingsDB.get()
        if data is not None:
            self.org_name.set(data.name)
            self.pos_head.set(data.pos_head)
            self.pos_coordinator.set(data.pos_coordinator)

    def save(self):
        SettingsDB.save(self.org_name.get(),
                        self.pos_head.get(),
                        self.pos_coordinator.get())
        self.destroy()
        self.update()

    def cancel(self):
        self.destroy()
        self.update()
