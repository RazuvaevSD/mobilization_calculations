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

        # 'Ctrl+c' и 'Ctrl-v' для русской раскладки в Windows
        app.event_add('<<Paste>>', '<Control-igrave>')
        app.event_add("<<Copy>>", "<Control-ntilde>")

        app.mainloop()

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
