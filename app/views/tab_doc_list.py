from tkinter import Menu, Menubutton, messagebox
from tkinter.ttk import Scrollbar, Treeview

from app.services.db.document import Document
from app.views.elements.protocol_win import Protocol
from app.views.tab_doc import TabDoc


class TabDocList:
    def __init__(self, tab_control) -> None:
        self.tab = tab_control.add_tab(id='doc_list',
                                       text='Документы')
        self.tab_control = tab_control
        self.create_menu()
        self.tree = self.create_tree()

        self.reload_tree()
        setattr(self.tab, 'reload_tree', self.reload_tree)

    def reload_tree(self):
        self.tree.delete(*self.tree.get_children())
        docs = Document.get_tree()
        for doc in docs:
            self.tree.insert(**doc)

        self.tree.tag_configure('parent', background='#98cbcd')
        self.tree.tag_configure('child', background='#d8f2f3')
        self.tree.tag_configure('non_child', background='silver')
        self.tree.tag_configure('non_parent', background='white')

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
            label='Расчет объемов (ОИВ)',
            background='white',
            command=lambda: self.create_document('amount_oiv')
        )
        create_menu.menu.add_command(
            label='Расчет объемов (свод)',
            background='white',
            command=lambda: self.create_document('amount_svod')
        )
        create_menu.menu.add_command(
            label='Расчет объемов (свод) на основе выбранных',
            background='white',
            command=self.create_document_by_selection
        )
        edit_menu = self.tab.menu.add_btn('edit_doc',  # noqa
                                          border=0,
                                          borderwidth=0,
                                          background='LightSteelBlue3',
                                          fg='black',
                                          activeforeground='white',
                                          activebackground='LightSteelBlue3',
                                          text='Редактировать выбранные',
                                          command=self.edit_document)
        edit_menu = self.tab.menu.add_btn('delete_doc',  # noqa
                                          border=0,
                                          borderwidth=0,
                                          background='LightSteelBlue3',
                                          fg='black',
                                          activeforeground='white',
                                          activebackground='LightSteelBlue3',
                                          text='Удалить выбранные',
                                          command=self.delete_document)

    def create_tree(self):
        """Создать дерево документов."""
        # Инициализация контрола
        columns = ('id', 'date', 'doc_type', 'organization')
        self.tree = Treeview(master=self.tab,
                             columns=columns,
                             show="tree headings")

        self.tree.column('id', minwidth=50, width=50, stretch='no')
        self.tree.column('date', minwidth=150, width=150, stretch='no')
        self.tree.column('doc_type', minwidth=170, width=200, stretch='no')
        self.tree.column('organization')

        self.tree.heading('id', text='id')
        self.tree.heading('date', text='Дата')
        self.tree.heading('doc_type', text='Документ')
        self.tree.heading('organization', text='Организация')

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

    def create_document(self, doc_type):
        """Отрыть форму создания документа."""
        if doc_type == 'amount_oiv':
            # если выбран документ ОИВ'а, просто открываем чистую форму
            tab = TabDoc(self.tab_control, doc_type=doc_type)
            tab.create_sheet(250, 6)
            self.tab_control.select(
                self.tab_control.get(
                    f'temp_id_{len(self.tab_control.tabs())-1}')
            )
        if doc_type == 'amount_svod':
            # если создается сводный документ
            # просто открываем чистую форму
            tab = TabDoc(self.tab_control, doc_type=doc_type)
            tab.create_sheet(250, 6)
            self.tab_control.select(
                self.tab_control.get(
                    f'temp_id_{len(self.tab_control.tabs())-1}')
            )

    def create_document_by_selection(self, doc_type='amount_svod'):
        """Создание сводного документа на основе выбранных."""
        selection = self.tree.selection()
        children = []
        fail_children = []
        for item in selection:
            if self.tree.item(item)['values'][2] == 'Расчет объемов (ОИВ)':
                # если есть выбранные документы,
                # то их id надо отсеять по типу 'Расчет объемов (ОИВ)'
                # и передать в новый таб, там сразу будет выполнен расчет
                if self.tree.parent(item):
                    protocol = Protocol(
                        'Предупреждение', '800x300',
                        'Один или несколько выбранных документов '
                        'уже входят в сводный документ. \n'
                        'Исключите их из выбора или удалите сводный.')
                    protocol.grab_set()
                    return
                children.append(item)
            else:
                fail_children.append(item)
        if len(children) < 1:
            protocol = Protocol(
                'Предупреждение!', '800x300',
                'Для создания документа "Расчет объемов (свод) на основе '
                'выбранных" необходимо выбрать документы "Расчет объемов '
                '(ОИВ)"\n\n'
                'Выбор выполняется зажатием клавиши "Сtrl"'
                'и выделением левой кнопкой мыши нужных строк.')
            protocol.grab_set()
            return
        tab = TabDoc(self.tab_control, doc_type=doc_type, children=children)
        tab.create_sheet(250, 6)
        tab.load_svod()
        self.tab_control.select(
            self.tab_control.get(
                f'temp_id_{len(self.tab_control.tabs())-1}')
        )
        if len(fail_children) > 0:
            protocol = Protocol(
                'Предупреждение!', '800x300',
                f'Вы выбрали один или несколько документов, являющихся'
                f'сводными.\nОни были исключены из расчета.\n'
                f'Вот перечень их id:\n {fail_children}')
            protocol.grab_set()

    def edit_document(self):
        """Отркыть документ для редактирования."""
        item = None
        selection = self.tree.selection()
        for item in selection:
            if item not in self.tab_control.tabs():
                # если документ еще не окрыт
                id = self.tree.item(item)['values'][0]
                doc_date = self.tree.item(item)['values'][1]
                doc_type = 'amount_oiv'
                if (self.tree.item(item)['values'][2] ==
                        'Расчет объемов (свод)'):
                    doc_type = 'amount_svod'

                tab = TabDoc(self.tab_control, id=id,
                             doc_type=doc_type,
                             text=f'{item} от {doc_date}')
                tab.create_sheet(250, 6)
                tab.load_doc_db()
                if len(self.tree.parent(item)) > 0:
                    # Если документ использован в сводном,
                    # блокируем табличную часть
                    tab.sheet.disable_bindings('all')

        if item is not None:
            # Если документ был уже открыт ранее
            self.tab_control.select(self.tab_control.get(item))

    def delete_document(self):
        """Удалить документ."""
        msg_box = messagebox.askquestion(
            title='Удаление документов.',
            message='Вы уверены что хотите удалить выбранные документы?',
            icon='warning')
        if msg_box == 'no':
            return
        # получить список id выделенных документов
        selection = self.tree.selection()
        if len(selection) < 1:
            protocol = Protocol(
                'Предупреждение', '800x300',
                'Для удаления выберите один или несколько документов.')
            protocol.grab_set()
            return

        for item in selection:
            # удалить документ
            Document.remove(item)
            # закрыть таб документа, если открыт
            self.tab_control.forget(item)

        self.reload_tree()
