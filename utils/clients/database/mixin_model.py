from utils.clients.database.create_model import CreateModel
from utils.clients.database.delete_model import DeleteModel
from utils.clients.database.filter_model import FilterModel
from utils.clients.database.update_model import UpdateModel


class MixinModel(
    FilterModel,
    CreateModel,
    UpdateModel,
    DeleteModel
):
    __abstract__ = True