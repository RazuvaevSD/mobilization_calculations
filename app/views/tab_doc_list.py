from tkinter import Menu, Menubutton
from tkinter.ttk import Scrollbar, Treeview

from .tab_doc import TabDoc


class TabDocList:
    def __init__(self, tab_control) -> None:
        self.tab_control = tab_control
        self.tab = tab_control.add_tab(id='doc_list',
                                       text='Документы')
        self.create_menu()
        self.tree = None

    def create_menu(self):
        create_menu = Menubutton(
            master=self.tab.menu,
            text='Создать \u23D0\u25BC',
            border=1,
            borderwidth=2,
            background='LightSteelBlue3',
            activeforeground='white',
            activebackground='LightSteelBlue3',
        )
        create_menu.menu = Menu(create_menu)
        create_menu["menu"] = create_menu.menu
        create_menu.pack(side='left', fill=None, padx=3)

        create_menu.menu.add_command(
            label='Создать док1',
            background='white',
            command=lambda: self.create_document()
        )
        create_menu.menu.add_command(
            label='Создать док2',
            background='white',
            command=lambda: self.create_document()
        )
        edit_menu = self.tab.menu.add_btn('edit_menu',  # noqa
                                          border=0,
                                          borderwidth=0,
                                          background='LightSteelBlue3',
                                          fg='black',
                                          activeforeground='white',
                                          activebackground='LightSteelBlue3',
                                          text='Редактировать выбранные',
                                          command=self.edit_document)

    def create_tree(self, columns, heads):
        """Создать дерево документов."""
        # Инициализация контрола
        self.tree = Treeview(master=self.tab,
                             columns=tuple(columns.keys()),
                             show="tree headings")

        for key, params in columns.items():
            self.tree.column(key, **params)
        for key, params in heads.items():
            self.tree.heading(key, **params)
        self.tree.column('#0', minwidth=50, width=50, stretch='no')
        self.tree.pack(fill='both', expand=1)

        # Добавить вертикальный скрол
        vert_scroll = Scrollbar(self.tree, orient="vertical",
                                command=self.tree.yview)
        vert_scroll.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vert_scroll.set)

        # Добавить горизонтальный скрол
        # (родителем указываем фрейм таба,
        # чтобы не перекрывал последнюю строку дерева)
        horiz_scroll = Scrollbar(self.tab, orient="horizontal",
                                 command=self.tree.xview)
        horiz_scroll.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=horiz_scroll.set)

        return self.tree

    def create_document(self):
        """Отрыть форму создания документа."""
        tab = TabDoc(self.tab_control)
        tab.create_sheet(250, 6)

    def edit_document(self):
        """Отркыть документ для редактирования."""
        for item in self.tree.selection():
            if item in self.tab_control.tabs():
                # Если документ уже открыт, перейти в его таб
                self.tab_control.select(self.tab_control.get(item))
            else:
                doc_date = self.tree.item(item)['values'][1]
                tab = TabDoc(self.tab_control, id=item,
                             text=f'{item} от {doc_date}')
                tab.create_sheet(250, 6)

    def delete_document():
        """Удалить документ."""
        ...
