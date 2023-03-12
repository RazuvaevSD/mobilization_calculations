import csv
import traceback
from os import path

from app.services.db.document import Document
from app.views.elements.protocol_win import Protocol


class CSVDocument:
    @staticmethod
    def write(doc_ids: list, folder: str):
        try:
            for id in doc_ids:
                doc_header_data, total_amount, amount_detail = (
                    Document.get_by_id(id)
                )
                filename = path.join(folder,
                                     f'{id} {doc_header_data.date}.csv')

                fileheader = [['data_type', 'name', 'type_expenses',
                               'amounts_transfer', 'amount_economy', 'total']]

                doc_header_data = [
                    ['doc_type', doc_header_data.doc_type],
                    ['date', doc_header_data.date],
                    ['number', doc_header_data.number],
                    ['org_name', doc_header_data.org_name],
                    ['pos_head', doc_header_data.pos_head],
                    ['pos_coordinator', doc_header_data.pos_coordinator],
                    ['annex', doc_header_data.annex],
                ]
                amount_data = [
                    [total_amount.data_type, total_amount.name,
                     total_amount.type_expenses, total_amount.amounts_transfer,
                     total_amount.amount_economy, total_amount.total],
                ]
                for amount in amount_detail:
                    amount_data.append([
                        amount.data_type, amount.name,
                        amount.type_expenses, amount.amounts_transfer,
                        amount.amount_economy, amount.total,
                    ])
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter='|',
                                        quoting=csv.QUOTE_NONE)
                    writer.writerows(fileheader)
                    writer.writerows(doc_header_data)
                    writer.writerows(amount_data)
            protocol = Protocol('Загрузка файлв!', '800x400',
                                'Файл(ы) успешно загружен(ы)!')
            protocol.grab_set()
        except Exception:
            protocol = Protocol('Ошибка загрузки файла!', '800x400',
                                traceback.format_exc())
            protocol.grab_set()
            return

    @staticmethod
    def read(list_filename: list):
        try:
            ids = []
            for filename in list_filename:
                with open(filename, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter='|')

                    doc_header_data = {
                        'doc_type': '',
                        'number': 1,
                        'date': '',
                        'org_name': '',
                        'pos_head': '',
                        'pos_coordinator': '',
                        'annex': '',
                    }
                    total_amount = {
                        'name': 'Итого в том числе:',
                        'type_expenses': '',
                        'amounts_transfer': '',
                        'amount_economy': '',
                        'total': '',
                    }
                    amount_detail = []
                    for row in reader:
                        if row['data_type'] in doc_header_data.keys():
                            doc_header_data[row['data_type']] = (
                                row['name'] or '')
                        if row['data_type'] == 'total':
                            total_amount = dict(row)
                        if row['data_type'] == 'detail':
                            amount_detail.append(dict(row))
                    doc_id = Document.save(id='temp_id_N',
                                           doc_header_data=doc_header_data,
                                           total_amount=total_amount,
                                           amount_detail=amount_detail)
                    if doc_id is not None:
                        ids.append(doc_id)
            if len(ids) > 0:
                return ids
        except Exception:
            protocol = Protocol('Ошибка загрузки файла!', '800x400',
                                traceback.format_exc())
            protocol.grab_set()
            return
