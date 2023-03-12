from app.core.config import WindowConf
from app.views.elements.window import Window
from app.views.settings import Setting
from app.views.tab_doc_list import TabDocList


class Aplication:
    def __init__(self):
        app = Window()
        app.title(WindowConf.TITLE.value),
        app.geometry(WindowConf.SIZE.value)
        self.initial_main_menu(app)

        app.bind("<Control-KeyPress>", self.keypress)

        app.mainloop()

    @staticmethod
    def keypress(event):
        """Обработчик событий горячих клавиш копипасты,
        (из-за русской раскладки в Windows)."""
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
        elif event.keycode == 88:
            event.widget.event_generate("<<Cut>>")

    @classmethod
    def initial_main_menu(cls, app):
        app.main_menu.add_btn(id='doc_list',
                              text='Список документов',
                              command=lambda: cls.open_doc_list(
                                    app.tab_control))
        app.main_menu.add_btn(id='settings',
                              text='Настройки',
                              command=cls.open_settings)

    @staticmethod
    def open_settings():
        settings = Setting()
        settings.grab_set()

    @staticmethod
    def open_doc_list(tab_control):
        TabDocList(tab_control=tab_control)
