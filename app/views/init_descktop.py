from app.core.config import WindowConf

from .elements.window import Window
from .tab_doc_list import TabDocList


def open_doc_list(tab_control):
    tab = TabDocList(tab_control=tab_control)

    columns = {
        'id': {'minwidth': 50, 'width': 50, 'stretch': 'no'},
        'date': {'minwidth': 150, 'width': 150, 'stretch': 'no'},
        'doc_type': {'minwidth': 150, 'width': 150, 'stretch': 'no'},
        'organization': {},
    }
    heads = {
        'id': {'text': 'id'},
        'date': {'text': 'Дата'},
        'doc_type': {'text': 'Документ'},
        'organization': {'text': 'Организация'}
    }

    tab.create_tree(columns=columns, heads=heads)

    tree = tab.tree
    parent = ''
    for i in range(1, 1001):
        # генерация тестовых данных
        doc = (
            i,
            '01.01.2020',
            f'doc_type {1 if i % 4 == 0 else 2}',
            f'Organization {i}')

        if i % 4 == 0:
            parent = i
        # Добавить данные
        tree.insert(parent=parent if i % 4 != 0 and i < 40 else '',
                    index='end',
                    iid=i,
                    values=doc,
                    tags=('parent' if i % 4 == 0 and i < 40 else 'child',))
        # Расскрасить
        tree.tag_configure('parent', background='#98cbcd')
        tree.tag_configure('child', background='white')


def initial_main_menu(master):
    master.main_menu.add_btn(id='doc_list',
                             text='Список документов',
                             command=lambda: open_doc_list(master.tab_control))


def initial_descktop_app():
    app = Window()
    app.title(WindowConf.TITLE.value),
    app.geometry(WindowConf.SIZE.value)
    initial_main_menu(app)

    app.mainloop()
