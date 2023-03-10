from app.crud.organization import organization_crud


class Settings:
    @staticmethod
    def save(org_name='', pos_head='', pos_coordinator=''):
        """Сохранить настройки в базу данных."""
        data = {
            'name': org_name,
            'pos_head': pos_head,
            'pos_coordinator': pos_coordinator
        }
        org = organization_crud.get_first()
        if org is not None:
            organization_crud.update(org, data)
            return
        organization_crud.create(data)
        return

    @staticmethod
    def get():
        """Получить настройки из базы данных."""
        data = organization_crud.get_list()
        if data is not None and len(data) > 0:
            return data[0]
        return None
