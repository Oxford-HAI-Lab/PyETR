import pyetr.data_parser.models as models
from pyetr.view import View

from .model_to_view import model_to_view
from .view_to_model import view_to_model


def view_to_json(v: View) -> str:
    return view_to_model(v).model_dump_json()


def json_to_view(s: str) -> View:
    return model_to_view(models.View.model_validate_json(s))
