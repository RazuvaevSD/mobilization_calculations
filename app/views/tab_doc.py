import re
from datetime import datetime
from tkinter import Entry, Frame, IntVar, Label, StringVar, messagebox

from tksheet import Sheet

from app.services.db.document import Document
from app.services.db.settings import Settings
from app.views.elements.protocol_win import Protocol

DT_FORMAT = '%d.%m.%Y'

HEADERS = (
    '№\nп/п',
    'Наименование',
    'ВР\n(группа,\nподгруппа,\nэлемент)',
    'на выполнение\nмероприятий\nПлана перевода\nна работу в условиях\n'
    'военного времени',
    'на выполнение\nмобилизационных\nзаданий (задач),\nустановленных\n'
    'Мобилизационным\nпланом экономики\nСахалинской области\n'
    'на расчетный период\nвоенного времени',
    'Всего')


class TabDoc:
    def __init__(self, tab_control, doc_type, id=None, text=None,
                 children=[]) -> None:
        """Инициализация таба документа.
        tab_control: экземпляр контроллера табов
        id: ID документа, если открывается документ на редактирование
        text: заголовок таба
        document_type: тип открываемого документа.
            Принимает значения:
                'amount_oiv' - документ органа власти
                'amount_svod' - сводный документ финансового органа
        children: список дочерних документов,
            если создается сводный из выбранных
        """
        self.doc_type = doc_type
        self.date = StringVar()
        self.inst = IntVar()
        self.org_name = StringVar()
        self.pos_head = StringVar()
        self.pos_coordinator = StringVar()
        self.tab_control = tab_control
        self.id = id
        self.is_new = False
        if self.id is None:
            # Если id не указан, значит создается новый документ
            self.id = f'temp_id_{len(self.tab_control.tabs())}'
            self.is_new
            self.load_default()
        self.children = children
        self.tab = tab_control.add_tab(id=self.id,
                                       text=text or 'Новый документ')
        self.create_menu()
        self.create_header(self.doc_type)
        self.sheet = None

    def load_default(self):
        """Загрузка значений по умолчанию для нового документа."""
        self.date.set(f'{datetime.now():{DT_FORMAT}}')
        self.inst.set(1)
        data = Settings().get()
        if data is not None:
            self.org_name.set(data.name)
            self.pos_head.set(data.pos_head)
            self.pos_coordinator.set(data.pos_coordinator)

    def create_menu(self):
        """Создать меню."""
        self.tab.menu.add_btn(id='doc_save',
                              text='Рассчитать и сохранить',
                              command=self.save_document,
                              background='LightSteelBlue3',
                              fg='black',
                              activeforeground='white',
                              activebackground='LightSteelBlue3',)
        self.tab.menu.add_btn(id='recalculation',
                              text='Расчет итогов',
                              command=self.recalculation,
                              background='LightSteelBlue3',
                              fg='black',
                              activeforeground='white',
                              activebackground='LightSteelBlue3',)
        self.tab.menu.add_btn(id='delete_document',
                              text='Удалить документ',
                              command=self.delete_document,
                              background='LightSteelBlue3',
                              fg='black',
                              activeforeground='white',
                              activebackground='LightSteelBlue3',)

    def create_header(self, doc_type):
        """Создать поля документа не входящих в табличную часть."""
        header = Frame(master=self.tab, background='white')
        header.pack(side='top', fill='x', ipadx=3, ipady=3)
        for c in range(20):
            header.columnconfigure(index=c, weight=1)
        for r in range(8):
            header.rowconfigure(index=r, weight=1)
        lbl_dt = Label(master=header, background='white',
                       text='Дата')
        lbl_dt.grid(row=0, column=0, padx=3, pady=1, sticky='w')
        txt_dt = Entry(master=header, background='white',
                       textvariable=self.date, state='disable')
        txt_dt.grid(row=1, column=0, padx=3, pady=1, sticky='w')

        lbl_instance = Label(master=header, background='white',
                             text='Экземпляр')
        lbl_instance.grid(row=0, column=1, padx=3, pady=1, sticky='w')
        txt_instance = Entry(master=header, background='white',
                             textvariable=self.inst)
        txt_instance.grid(row=1, column=1, padx=3, pady=1, sticky='w')
        if doc_type == 'amount_oiv':
            lbl_name_oiv = Label(master=header, background='white',
                                 text='Наименование ОИВ (в дательном падеже)')
            lbl_name_oiv.grid(row=2, column=0, padx=3, pady=1, sticky='w',
                              columnspan=2)
            txt_name_oiv = Entry(master=header, background='white',
                                 width=45, textvariable=self.org_name)
            txt_name_oiv.grid(row=3, column=0, padx=3, pady=1, sticky='w',
                              columnspan=2)

            lbl_position_head = Label(master=header, background='white',
                                      text='Должность руководителя ОИВ')
            lbl_position_head.grid(row=2, column=2, padx=3, pady=1, sticky='w',
                                   columnspan=2)
            txt_position_head = Entry(master=header, background='white',
                                      width=45, textvariable=self.pos_head)
            txt_position_head.grid(row=3, column=2, padx=3, pady=1, sticky='w',
                                   columnspan=2)

            lbl_position_coordinator = Label(master=header,
                                             background='white',
                                             text='Должность согласующего')
            lbl_position_coordinator.grid(row=4, column=0, padx=3, pady=1,
                                          sticky='w', columnspan=2)
            txt_position_coordinator = Entry(master=header,
                                             textvariable=self.pos_coordinator,
                                             background='white', width=45)
            txt_position_coordinator.grid(row=5, column=0, padx=3, pady=1,
                                          sticky='w', columnspan=2)

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
            newheaders=HEADERS,
            index=-1,
            reset_col_positions=False,
            show_headers_if_not_sheet=True,
            redraw=False)
        # установить ширину колонок
        self.sheet.column_width(column=0, width=50, redraw=True)
        self.sheet.column_width(column=1, width=300, redraw=True)
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
        if value is None or value == '':
            return value, 'Err', 'Значение не может быть пустым.'
        pattern = re.compile(r'^\d+$')
        if pattern.fullmatch(value) is None:
            return value, 'Err', 'Значение должно быть целым числом.'
        return value, 'OK', None

    @staticmethod
    def validate_name(value):
        """Валидация суммы."""
        if value is None or value == '':
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
            value, status, msg = self.validate_type_exp(value)
            if status != 'OK':
                return ''
        if event.column in [3, 4]:
            # проверить формат суммы
            value, status, msg = self.validate_amount(value=value)
            if status != 'OK':
                return '0'
        return value

    def set_number_in_sequence(self, row):
        for i in range(1, row + 1):
            self.sheet.set_cell_data(
                i, 0, value=f'{i}',
                # set_copy=True,
                # redraw=True,
            )

    def recalculation(self, protocol_mode=True):
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
                # если валидация не пройдена формируем текст вывода протокола
                msg += f'\nСтрока {i+1}:'
                for val in row_protocol:
                    msg += (f'\n    поле "{val[0]}", значение'
                            f' "{val[1]}", ошибка "{val[2]}"')
        if len(msg) > 0:
            # при налиции сообщения выводим протокол
            message = Protocol(title='Расчет итогов невозможен.',
                               geometry='1200x400',
                               message=msg)
            message.grab_set()
            return

        # Расчет колонки Всего
        for i in range(len(data)):
            if i == 0 or len(''.join(data[i])) < 1:
                continue
            data[i][5] = str(int(data[i][3]) + int(data[i][4]))

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
        if protocol_mode:
            message = Protocol(title='Расчет итогов завершен.',
                               geometry='800x300',
                               message='Расчет итогов успешно завершен.')
            message.grab_set()

    def load_doc_db(self):
        """Загрузить документ из базы."""
        if 'temp_id_' in str(self.id):
            return
        doc_header_data, total_amount, amount_detail = Document.get_by_id(
            self.id)
        # заполнить заголовок
        self.doc_type = doc_header_data.doc_type
        self.inst.set(doc_header_data.number)
        self.date.set(doc_header_data.date)
        self.org_name.set(doc_header_data.org_name)
        self.pos_head.set(doc_header_data.pos_head)
        self.pos_coordinator.set(doc_header_data.pos_coordinator)
        # сформировать табличную часть
        data = []
        # итоговая строка
        data.append([
            '',
            total_amount.name,
            total_amount.type_expenses,
            total_amount.amounts_transfer,
            total_amount.amount_economy,
            total_amount.total])
        # строки с детализацией
        counter = 0
        for amount in amount_detail:
            counter += 1
            data.append([
                str(counter),
                amount.name,
                amount.type_expenses,
                amount.amounts_transfer,
                amount.amount_economy,
                amount.total])
        # Заполнить таблицу данными
        self.sheet.set_sheet_data(data=data,
                                  reset_col_positions=False,
                                  reset_row_positions=True,
                                  redraw=True)
        # self.sheet.total_rows(250)
        # здесь ошибка у автора библиотеки
        # при mode_position=True в функции GetLinesHeight
        # он сравнивает n > 1 где n это tuple
        # приэтом при mode_position=False строки не добавляются вообще..
        # дальше не ковырял
        total_rows = self.sheet.get_total_rows()
        for i in range(250-total_rows):
            # 250 на вскидку с запасом
            # чтобы пользователь не утруждалсядобавлением новых строк
            self.sheet.insert_row(idx='end', redraw=True)

    def load_svod(self):
        data = Document.get_svod(self.children)

        self.sheet.set_sheet_data(data=data,
                                  reset_col_positions=False,
                                  reset_row_positions=True,
                                  redraw=True)

        total_rows = self.sheet.get_total_rows()
        for i in range(250-total_rows):
            self.sheet.insert_row(idx='end', redraw=True)

    def save_document(self):
        """Сохранить документ."""
        try:
            self.recalculation(protocol_mode=False)
            # сформировать заголовок
            doc_header_data = {
                'doc_type': self.doc_type,
                'number': self.inst.get(),
                'date': self.date.get(),
                'org_name': self.org_name.get() or '',
                'pos_head': self.pos_head.get() or '',
                'pos_coordinator': self.pos_coordinator.get() or ''}
            # сформировать итоговую строку
            total = self.sheet.get_row_data(r=0)
            total_amount = {
                'name': total[1],
                'type_expenses': total[2],
                'amounts_transfer': total[3],
                'amount_economy': total[4],
                'total': total[5]}
            # сформировать детализированные данные
            data = list(self.sheet.get_sheet_data())
            data.pop(0)  # убираем итоговую строку
            amount_data = []
            for row in data:
                if len(''.join(row)) < 1:
                    # пропустить пустые строки
                    continue
                amount_data.append({
                    'name': row[1],
                    'type_expenses': row[2],
                    'amounts_transfer': row[3],
                    'amount_economy': row[4],
                    'total': row[5]})
            self.id = Document.save(id=self.id,
                                    doc_header_data=doc_header_data,
                                    children=self.children,
                                    total_amount=total_amount,
                                    amount_detail=amount_data)
            # обновить таб "Список документов" если он открыт
            tab_doc_list = self.tab_control.get('doc_list')
            if tab_doc_list is not None:
                tab_doc_list.children['!treeview']
                tab_doc_list.reload_tree()
        except Exception as ex:
            protocol = Protocol('Ошибка при сохранении!', '800x300', ex)
            protocol.grab_set()
            return
        protocol = Protocol('Сохранение', '800x300',
                            'Расчет итогов и сохранение выполнены успешно!')

    def delete_document(self):
        """Удалить документ."""
        msg_box = messagebox.askquestion(
            title='Удаление документа.',
            message='Вы уверены что хотите удалить текущий документ?',
            icon='warning')
        if msg_box == 'no':
            return
        Document.remove(self.id)

        # обновить таб "Список документов" если он открыт
        tab_doc_list = self.tab_control.get('doc_list')
        if tab_doc_list is not None:
            tab_doc_list.children['!treeview']
            tab_doc_list.reload_tree()

        # Закрыть текущую вкладку
        id = None
        if self.is_new and 'temp_id' in self.id:
            # если документ удаляется в том же табе что и создавался
            id = f'temp_id{self.id}'
        else:
            id = self.id
        self.tab_control.forget(id)
        self.tab_control.event_generate('<<NotebookTabClosed>>')
