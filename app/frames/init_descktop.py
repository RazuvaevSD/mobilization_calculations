from tkinter import LEFT, Frame, Label, Menu, Menubutton

from app.core.config import WindowConf
from app.frames import MainMenu, TabControl, Window


def foo(a):
    print('print test text', a)


def open_tab(tab_control):
    """Open tab for documents list or one document.
    Args:
        tab_control (_type_): _description_
        mode (str, optional): 'doc' for documents;
                              'doc_list' for documents list.
                              Defaults to 'doc'.
    """
    tab_control.add_tab(id=1321, text='asdfasdf \n')
    tab_control.add_tab(id='unique_name2', text='asdfasdf \n')

    ####################################################
    #                   T E S T                        #
    ####################################################
    tabmenu = Frame(master=tab_control.get(1321), bg='steel blue', padx=2, pady=3)
    tabmenu.pack(side='top', fill='x')
    menubutton = Menubutton(tabmenu, text="Создать \u23D0\u25BC")
    menubutton.menu = Menu(menubutton)
    menubutton["menu"] = menubutton.menu
    # menu = Menu(tab_control.get(1321))
    menubutton.menu.add_command(label='Создать док1')
    menubutton.menu.add_command(label='Создать док2')
    menubutton.pack(side='left', fill=None)

    lbl_test = Label(master=tab_control.get('1321'),
                     text='test_text', bg='white')
    lbl_test.pack()


def bar():
    ...
    # tab_doc_list = tab_control.children.get('main_tab')
    # print(tab_control.children)
    # tab = tab_control.children.get('tab_doc_list')
    # print(tab)
    # tab_frame = tab.children.get('tab_frame_doc_list')
    # print(tab_frame)


def initial_descktop_app():
    app = Window()
    app.title(WindowConf.TITLE.value),
    app.geometry(WindowConf.SIZE.value)

    # Добавляем меню
    main_menu = MainMenu(master=app)
    main_menu.add_command(label='Список документов')
    app.config(menu=main_menu)

    tab_control = TabControl(master=app.main_frame)
    # привяжем функцию открытия таба для списка документов
    # т.к. она заранее предопределена
    main_menu.entryconfigure(0, command=lambda: open_tab(tab_control))

    app.mainloop()
