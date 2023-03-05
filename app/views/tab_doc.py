from tksheet import Sheet


class TabDoc:
    def __init__(self, tab_control, id=None, text=None) -> None:
        self.tab_control = tab_control
        if id is None:
            id = f'temp_id_{len(self.tab_control.tabs())}'
        self.tab = tab_control.add_tab(id=id,
                                       text='Документ')
        self.create_menu()
        self.sheet = None

    def create_menu(self):
        self.tab.menu.add_btn(id='doc_save',
                              text='Сохранить')

    def create_table(self, rows, columns):
        """Создать таблицу документа."""
        self.sheet = Sheet(self.tab)
        self.sheet.enable_bindings()
        self.sheet.insert_rows(rows=rows,
                               idx='end')
        self.sheet.insert_column(columns=columns)
        self.sheet.pack(fill='both', expand=True)

    def delete_document():
        """Удалить документ."""
        ...

    def save_document():
        """Сохранить документ."""
        ...
