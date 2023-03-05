# импорты для alembic (т.к. модели не в одном файле, импортировать стоит здесь)
from app.core.db import Base  # noqa
from app.models.amount import Amount  # noqa
from app.models.document import Document  # noqa
from app.models.document_type import DocumentType  # noqa
from app.models.organization import Organization  # noqa
