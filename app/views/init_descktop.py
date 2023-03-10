from app.core.config import WindowConf
from app.views.elements.window import Window
from app.views.settings import Setting
from app.views.tab_doc_list import TabDocList


def open_doc_list(tab_control):
    TabDocList(tab_control=tab_control)


def open_settings():
    settings = Setting()
    settings.grab_set()


def initial_main_menu(app):
    app.main_menu.add_btn(id='doc_list',
                             text='Список документов',
                             command=lambda: open_doc_list(app.tab_control))
    app.main_menu.add_btn(id='settings',
                             text='Настройки',
                             command=open_settings)


def initial_descktop_app():
    app = Window()
    app.title(WindowConf.TITLE.value),
    app.geometry(WindowConf.SIZE.value)
    initial_main_menu(app)

    app.mainloop()
