from tkinter import Frame, PhotoImage
from tkinter.ttk import Notebook, Style


class TabWithCloseButton(Notebook):
    """Таб-контрол с кнопкой закрытия."""
    # Стянул на просторах интернета,
    # разбираться как делать свой не хватает времени
    # https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook
    __initialized = False

    def __init__(self, with_close_button=True, *args, **kwargs):
        if not self.__initialized:
            if with_close_button:
                self.__initialize_custom_style()
            self.__inititialized = True

        if with_close_button:
            kwargs['style'] = 'CustomNotebook'
        Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind('<ButtonPress-1>', self.on_close_press, True)
        self.bind('<ButtonRelease-1>', self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if 'close' in element:
            index = self.index('@%d,%d' % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return 'break'
        return None

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if 'close' not in element:
            # user moved the mouse off of the close button
            return

        index = self.index('@%d,%d' % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate('<<NotebookTabClosed>>')

        self.state(['!pressed'])
        self._active = None

    def __initialize_custom_style(self):
        style = Style()
        self.images = (
            PhotoImage('img_close', data="""
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                """),
            PhotoImage('img_closeactive', data="""
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                """),
            PhotoImage('img_closepressed', data="""
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            """)
        )

        style.element_create('close', 'image', 'img_close',
                             ('active', 'pressed', '!disabled',
                              'img_closepressed'),
                             ('active', '!disabled', 'img_closeactive'),
                             border=8, sticky='')
        style.layout('CustomNotebook',
                     [('CustomNotebook.client',
                       {'sticky': 'nswe'})])
        style.layout('CustomNotebook.Tab', [
            ('CustomNotebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('CustomNotebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('CustomNotebook.focus', {
                                'side': 'top',
                                'sticky': 'nswe',
                                'children': [
                                    ('CustomNotebook.label',
                                     {'side': 'left', 'sticky': ''}),
                                    ('CustomNotebook.close',
                                     {'side': 'left', 'sticky': ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])


class TabControl(TabWithCloseButton):
    def __init__(self, with_close_button=True, *args, **kwargs):
        super().__init__(with_close_button, *args, **kwargs)
        super().pack(fill='both', expand=1)

    def add_tab(self, menu: Frame = None, background='white', **kw):
        frame = Frame(master=self, bg=background)
        frame.pack(fill='both', expand=True)
        self.add(child=frame, **kw)
        if menu is not None:
            menu = menu
        return frame
