from falconer.models.inventory import Actor, Film
from falconer.resources.base import BaseResource
from falconer.schemas.inventory import ActorSchema, FilmSchema


class ActorResource(BaseResource):
    schema_cls = ActorSchema
    model_cls = Actor
    singular = 'Actor'
    plural = 'Actors'


class FilmResource(BaseResource):
    schema_cls = FilmSchema
    model_cls = Film
    singular = 'Film'
    plural = 'Films'
