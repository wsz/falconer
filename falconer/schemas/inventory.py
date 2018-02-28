from falconer.models import inventory as model
from falconer.schemas.base import BaseSchema


class ActorSchema(BaseSchema):
    class Meta:
        model = model.Actor


class FilmSchema(BaseSchema):
    class Meta:
        model = model.Film
