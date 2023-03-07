import re

from tksheet import Sheet

from app.views.elements.protocol_win import Protocol


class TabDoc:
    def __init__(self, tab_control, id=None, text=None) -> None:
        self.tab_control = tab_control
        if id is None:
            id = f'temp_id_{len(self.tab_control.tabs())}'
        self.tab = tab_control.add_tab(id=id,
                                       text=text or 'Документ')
        self.create_menu()
        self.sheet = None
        if id is not None:
            self.load_doc_db()

    def create_menu(self):
        self.tab.menu.add_btn(id='doc_save',
                              text='Сохранить',
                              command=self.save_document,
                              background='LightSteelBlue3',
                              fg='black',
                              activeforeground='white',
                              activebackground='LightSteelBlue3',)
        self.tab.menu.add_btn(id='recalculation',
                              text='Расчет итогов',
                              command=self.recalculation)

    def create_sheet(self, rows, columns):
        """Создать таблицу документа."""

        self.sheet = Sheet(self.tab,
                           total_rows=rows,
                           total_columns=columns,
                           header_height=170,
                           expand_sheet_if_paste_too_big=False)
        self.sheet.enable_bindings()
        # Задать заголовок
        self.sheet.headers(
            newheaders=('№\nп/п',
                        'Наименование',
                        'ВР\n(группа,\nподгруппа,\nэлемент)',
                        'на выполнение\nмероприятий\nПлана перевода\n'
                        'на работу в условиях\nвоенного времени',
                        'на выполнение\nмобилизационных\nзаданий (задач),\n'
                        'установленных\nМобилизационным\nпланом экономики\n'
                        'Сахалинской области\nна расчетный период\nвоенного'
                        ' времени',
                        'Всего'),
            index=-1,
            reset_col_positions=True,
            show_headers_if_not_sheet=True,
            redraw=False)
        # установить ширину колонок
        self.sheet.column_width(column=0, width=50, redraw=True)
        self.sheet.column_width(column=1, width=200, redraw=True)
        self.sheet.column_width(column=2, width=100, redraw=True)
        self.sheet.column_width(column=3, width=170, redraw=True)
        self.sheet.column_width(column=4, width=170, redraw=True)
        self.sheet.column_width(column=5, width=100, redraw=True)
        # вставить первой итоговую строку
        self.sheet.insert_row(
            values=['', 'Итого, в том числе:'],
            idx=0)

        self.sheet.extra_bindings('end_edit_cell',
                                  func=self.cell_validate)
        self.sheet.pack(fill='both', expand=True)

    @staticmethod
    def validate_type_exp(value):
        """Валидация кода вида расходов."""
        if value is None and value == '':
            return value, 'Err', 'Значение не может быть пустым.'
        pattern = re.compile(r'^^[1-9]((00)|([1-9][0-9]))$')
        if pattern.fullmatch(value) is None:
            return (value, 'Err',
                    'Значение не соответствует формату "NMX",'
                    'где: "N" - группа, "M" - подгруппа, "X" - элемент.')
        return value, 'OK', None

    @staticmethod
    def validate_amount(value):
        """Валидация суммы."""
        if value is None and value == '':
            return value, 'Err', 'Значение не может быть пустым.'
        pattern = re.compile(r'^\d+$')
        if pattern.fullmatch(value) is None:
            return value, 'Err', 'Значение должно быть целым числом.'
        return value, 'OK', None

    @staticmethod
    def validate_name(value):
        """Валидация суммы."""
        if value is None and value == '':
            return value, 'Err', 'Значение не может быть пустым.'
        return value, 'OK', None

    def validate(self, row_data):
        protocol = []
        field, value, status, msg = None, None, None, None
        for i in range(len(row_data)):
            field, value, status, msg = None, None, None, None
            if i == 1:
                field = 'Наименование'
                value, status, msg = self.validate_name(row_data[i])
            if i == 2:
                field = 'Код вида расходов'
                value, status, msg = self.validate_type_exp(row_data[i])
            if i in [3, 4]:
                field = 'Сумма плана перевода' if i == 3 else ('Сумма плана '
                                                               'экономики.')
                value, status, msg = self.validate_amount(row_data[i])
            if status is not None and status != 'OK':
                protocol.append((field, value, msg))
        return protocol

    def cell_validate(self, event=None):
        """Валидация вводимых значений."""
        if event is None:
            return None
        self.set_number_in_sequence(event.row)
        if event.row == 0:
            # Запрет ввода в первую строку
            if event.column == 1:
                return 'Итого, в том числе:'
            return ''
        if event.column == 0:
            # Запрет ввода в колонку номера по порядку
            return str(event.row)
        if event.column == 5:
            # Атозаполнение колонки всего при попытке ввести свое значение
            data = self.sheet.get_row_data(r=event.row)
            self.set_number_in_sequence(event.row)
            return str(int(data[3] or '0') + int(data[4] or '0'))
        value = event.text
        if event.column == 2:
            # Проверить формат вида расходов
            if value is not None and value != '':
                pattern = re.compile(r'^^[1-9]((00)|([1-9][0-9]))$')
                if pattern.fullmatch(value) is None:
                    return ''
        if event.column in [3, 4]:
            # проверить формвт суммы
            if value is None or value == '':
                value = '0'
            pattern = re.compile(r'^\d+$')
            if pattern.fullmatch(value) is None:
                return '0'
            else:
                value = value
        return value

    def set_number_in_sequence(self, row):
        for i in range(1, row + 1):
            self.sheet.set_cell_data(
                i, 0, value=F'{i}',
                set_copy=True,
                redraw=False
            )

    def recalculation(self):
        """Расчет итогов."""
        data = self.sheet.get_sheet_data()
        # Валидация
        msg = ''
        for i in range(len(data)):
            if i == 0:
                # пропустить итоговую строку
                continue
            if len(''.join(data[i])) < 1:
                # пропустить пустые строки
                continue
            row_protocol = self.validate(data[i])
            if len(row_protocol) > 0:
                msg += f'\nСтрока {i+1}:'
                for val in row_protocol:
                    msg += (f'\n    поле "{val[0]}", значение'
                            f' "{val[1]}", ошибка "{val[2]}"')
        if len(msg) > 0:
            message = Protocol(title='Расчет итогов невозможен.',
                               geometry='1200x400',
                               message=msg)
            message.grab_set()
            return

        # Расчет колонки Всего
        for i in range(len(data)):
            if i == 0 or len(''.join(data[i])) < 1:
                continue
            data[i][5] = int(data[i][3]) + int(data[i][4])

        # Расчет итоговой строки
        col_3 = sum([int(row[3]) if row[3] != '' else 0 for row in data[1:]])
        col_4 = sum([int(row[4]) if row[4] != '' else 0 for row in data[1:]])
        sum_1 = str(col_3)
        sum_2 = str(col_4)
        sum_3 = str(col_3 + col_4)
        data[0] = ['', 'Итого в том числе:', '', sum_1, sum_2, sum_3]
        # Обновить данные
        self.sheet.set_sheet_data(data=data,
                                  reset_col_positions=False,
                                  reset_row_positions=False)

        # Вывод сообщения об успехе.
        message = Protocol(title='Расчет итогов завершен.',
                           geometry='300x300',
                           message='Расчет итогов успешно завершен.')
        message.grab_set()

    def load_doc_db(self):
        """Загрузить документ из базы."""
        ...

    def delete_document(self):
        """Удалить документ."""
        ...

    def save_document(self):
        """Сохранить документ."""
        print(self.sheet.get_sheet_data())
        print(self.sheet.headers())
