from app.crud.amount import amount_crud  # noqa
from app.crud.document import document_crud  # noqa


class Document:
    @staticmethod
    def save(id,  doc_header_data, children=None,
             total_amount={}, amount_detail=[]):
        """Сохранить документ в базу данных."""
        doc_id = id
        if 'temp_id_' in str(id):
            # Если документ новый
            doc = document_crud.create(doc_header_data)
            doc_id = doc.id
            if total_amount is not None:
                # Если передана итоговая строка
                total_amount['data_type'] = 'total'
                total_amount['document_id'] = doc_id
                amount_crud.create(total_amount)
            if amount_detail is not None:
                # Если передан список строк с детализацией
                for amount in amount_detail:
                    amount['data_type'] = 'detail'
                    amount['document_id'] = doc_id
                    amount_crud.create(amount)
        else:
            doc_id = int(doc_id)
            doc = document_crud.get(id)
            doc = document_crud.update(doc, doc_header_data)
            doc_id = doc.id
            if len(total_amount) > 0:
                # Если передана итоговая строка
                amount_crud.remove_by_doc(doc_id, 'total')
                total_amount['data_type'] = 'total'
                total_amount['document_id'] = doc_id
                amount_crud.create(total_amount)
            if len(amount_detail) > 0:
                # Если передан список строк с детализацией
                amount_crud.remove_by_doc(doc_id, 'detail')
                for amount in amount_detail:
                    amount['data_type'] = 'detail'
                    amount['document_id'] = doc_id
                    amount_crud.create(amount)
        if children is not None:
            for child_id in children:
                doc = document_crud.get(child_id)
                data = {'parent_id': doc_id}
                document_crud.update(doc, data)
        return doc_id

    @staticmethod
    def get_by_id(doc_id):
        """Получить документ из базы данных по id."""
        if 'temp_id_' in str(doc_id):
            # если попытка загрузить несохраненный документ
            return
        doc_id = int(doc_id)
        doc_header_data = document_crud.get(doc_id)
        total_amount = amount_crud.get_by_type(doc_id, 'total').first()
        amount_detail = amount_crud.get_by_type(doc_id, 'detail').all()
        return doc_header_data, total_amount, amount_detail

    @staticmethod
    def get_tree():
        """Получить список документов подготовленный для вставки в TreeView."""
        tree = []
        docs = document_crud.get_list_non_children()
        for doc in docs:
            children = document_crud.get_child(doc.id)
            is_parent = 'non_parent'
            if len(children) > 0:
                is_parent = 'parent'
            elif doc.doc_type == 'amount_svod':
                is_parent = 'non_child'
            else:
                is_parent = 'non_parent'

            doc_type = 'Расчет объемов (свод)'
            if doc.doc_type == 'amount_oiv':
                doc_type = 'Расчет объемов (ОИВ)'

            tree.append({
                'parent': '',
                'index': 'end',
                'iid': doc.id,
                'values': (
                    doc.id,
                    doc.date,
                    doc_type,
                    doc.org_name
                ),
                'tags': (is_parent,)
            })

            for chldren in children:
                doc_type = 'Расчет объемов (свод)'
                if chldren.doc_type == 'amount_oiv':
                    doc_type = 'Расчет объемов (ОИВ)'
                tree.append({
                    'parent': chldren.parent_id,
                    'index': 'end',
                    'iid': chldren.id,
                    'values': (
                        chldren.id,
                        chldren.date,
                        doc_type,
                        chldren.org_name
                    ),
                    'tags': ('child',)
                })
        return tree

    @staticmethod
    def get_svod(list_id):
        """Получить свод из указанных документов."""
        # получить и сформировать итоговую строку
        total = amount_crud.get_svod_total(list_id)
        data = [[
            '', 'Итого в том числе:', '',
            *list(map(str, total))
        ]]
        # получить и сформировать свод по видам расходов
        amount = amount_crud.get_svod(list_id)
        counter = 0
        for row in amount:
            counter += 1
            data.append([
                str(counter), *list(map(str, row))
            ])
        return data

    @staticmethod
    def remove(id):
        """Удалить документ по указанному id."""
        if 'temp_id_' in str(id):
            # если попытка удалить несохраненный документ
            return
        # отвязать дочерние документы
        id = int(id)
        children = document_crud.get_child(id)
        for child in children:
            data = {'parent': None}
            document_crud.update(child, data)
        # удалить строки табличной части документа
        amount_crud.remove_by_doc(doc_id=id, data_type='total')
        amount_crud.remove_by_doc(doc_id=id, data_type='detail')
        # удалить документ
        doc = document_crud.get(id)
        document_crud.remove(doc)
