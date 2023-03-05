from tkinter import Frame, PhotoImage
from tkinter.ttk import Notebook, Style

from .menu import MenuControl


class TabWithCloseButton(Notebook):
    """Таб-контрол с кнопкой закрытия."""
    # В данном классе переопределена только функция закрытия
    # остальное в TabControl
    #
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

    def get(self, id):
        """(добавленная) Получить фрейм таба по его ИД"""
        id = str(id).lower()
        if id not in self.children:
            raise ValueError(f'Таб с идентификатором \'{id}\' не найден.')
        return self.children[id]

    def forget(self, id) -> None:
        """(переопределенная) Удалить таб по ИД"""
        tab = self.get(id)
        super().forget(tab)
        if tab in self.children:
            del self.children[tab]

    def tabs(self):
        """(переопределенная) Получить словарь с табами."""
        return self.children

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
            tab_id = super().tabs()[index].split('.')[-1]
            self.forget(tab_id)
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
                                     {'side': 'bottom', 'sticky': ''}),
                                    ('CustomNotebook.close',
                                     {'side': 'right', 'sticky': ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
        theme = style.theme_use()
        style.theme_settings(
            theme,
            settings={
                "CustomNotebook": {
                    "configure": {
                        "background": '#e0e0e0',
                        "tabmargins": [5, 5, 0, 0],
                        "borderwidth": 2,
                    }
                },
                "CustomNotebook.Tab": {
                    "configure": {
                        "background": '#f2f2f2',
                        "padding": [5, 2],
                        "font": "black",
                    },
                    "map": {
                        "background": [("selected", 'white')],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                }
            })


class TabControl(TabWithCloseButton):
    """Таб-контрол с кнопкой закрытия."""
    # Здесь переопределена основная функциональность работы с табами
    # кроме функции закрытия которая переопределена в родительском классе
    def __init__(self, with_close_button=True, *args, **kwargs):
        super().__init__(with_close_button,
                         *args, **kwargs)
        super().pack(fill='both', expand=1)

    def add_tab(self, id, background='white', menu: Frame = None, **kw):
        """Создание таба с контроллером меню"""
        tab = self.Tab(master=self, name=str(id).lower(), bg=background)
        tab.pack(fill='both', expand=True)
        self.add(child=tab, **kw)
        # добавляем в таб контроллер меню
        menu = MenuControl(master=tab,
                           bg='steel blue',
                           padx=2, pady=2)
        # для быстрого доступа добавим табу атрибут-ссылку на контроллер меню
        setattr(tab, 'menu', menu)
        return tab

    class Tab(Frame):
        pass
