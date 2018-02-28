from typing import Type

import falcon

from falcon import Request, Response
import simplejson as json
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from falconer.db.model import Base
from falconer.schemas.base import BaseSchema
from falconer.codecs import ImprovedJSONEncoder


LIST_HANDLING_METHODS = ['GET', 'POST']
RESOURCE_HANDLING_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']


class BaseResource:
    schema_cls: Type[BaseSchema] = None
    session: Session = None
    model_cls: Type[Base] = None
    singular: str = None
    plural: str = None

    def on_get(self, req: Request, resp: Response, resource_id=None):
        self._read(req, resp, resource_id)

    def on_delete(self, req: Request, resp: Response, resource_id=None):
        self._raise_for_list(resource_id)

        self._delete(req, resp, resource_id)

    def on_put(self, req: Request, resp: Response, resource_id=None):
        self._raise_for_list(resource_id)

        self._update(req, resp, resource_id)

    def on_patch(self, req: Request, resp: Response, resource_id=None):
        self._raise_for_list(resource_id)

        self._update(req, resp, resource_id, partial=True)

    def on_post(self, req: Request, resp: Response, resource_id=None):
        self._raise_for_resource(resource_id)

        self._create(req, resp)

    def on_options(self, req, resp, resource_id=None):
        result = {
            'name': self.plural if resource_id else self.singular,
            'fields': {
                key: self._serialize_schema_field(value) for key, value in self.schema_cls._declared_fields.items()
            }
        }

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200

    @property
    def _query(self):
        return self.session.query(self.model_cls)

    def _raise_for_list(self, resource_id):
        if not resource_id:
            raise falcon.HTTPMethodNotAllowed(LIST_HANDLING_METHODS)

    def _raise_for_resource(self, resource_id):
        if resource_id:
            raise falcon.HTTPMethodNotAllowed(RESOURCE_HANDLING_METHODS)

    def _get_for_update(self, resource_id):
        inspection_obj = inspect(self.model_cls)
        primary_column = inspection_obj.primary_key[0]  # TODO: assuming primary key is not composite
        primary_prop = inspection_obj.mapper.get_property_by_column(primary_column)

        return self._query.with_for_update(read=True).filter_by(**{primary_prop.key: resource_id}).one()

    def _create(self, req, resp):
        schema = self.schema_cls()
        deserialized = json.load(req.bounded_stream)
        parsed = schema.load(deserialized, session=self.session)

        if parsed.errors:
            raise falcon.HTTPUnprocessableEntity(description=parsed.errors)

        try:
            self.session.add(parsed.data)
            self.session.flush()
        except SQLAlchemyError as err:
            raise falcon.HTTPUnprocessableEntity(description='Database error') from err

        resp.body = json.dumps(parsed.data.id, cls=ImprovedJSONEncoder)
        resp.status = falcon.HTTP_201

    def _read(self, req, resp, resource_id):
        compact = req.get_param_as_bool('compact')

        schema = self.schema_cls(many=resource_id is None)

        if schema.many:
            page = req.get_param_as_int('page') or 1
            page_size = req.get_param_as_int('page_size') or 10
            sorting_params = req.get_param_as_list('sort', transform=lambda param: param.split(':'))

            result = self._query

            if sorting_params:
                sorting = self._parse_sorting_params(sorting_params)
                result = result.order_by(*sorting)

            result = result.offset((page - 1) * page_size).limit(page_size)
        else:
            result = self._query.get(resource_id)
            if not result:
                raise falcon.HTTPNotFound()

        marshalled = schema.dump(result)
        serialized = json.dumps(marshalled.data, cls=ImprovedJSONEncoder, indent=None if compact else 4)  # or schema.dumps()
        resp.body = serialized
        resp.status = falcon.HTTP_200

    def _update(self, req, resp, resource_id, partial=False):
        resource = self._get_for_update(resource_id)
        if not resource:
            raise falcon.HTTPNotFound()

        schema = self.schema_cls(instance={})
        deserialized = json.load(req.bounded_stream)
        parsed = schema.load(deserialized, session=self.session, instance=resource, partial=partial)

        if parsed.errors:
            raise falcon.HTTPUnprocessableEntity(description=parsed.errors)

        try:
            self.session.flush()
        except SQLAlchemyError as err:
            raise falcon.HTTPUnprocessableEntity(description='Database error') from err

        resp.status = falcon.HTTP_204

    def _delete(self, req, resp, resource_id):
        resource = self._query.get(resource_id)
        if not resource:
            raise falcon.HTTPNotFound()

        self.session.delete(resource)

        resp.status = falcon.HTTP_204

    def _parse_sorting_params(self, params):
        results = []

        inspection_obj = inspect(self.model_cls)

        mapped_columns = [attr.key for attr in inspection_obj.mapper.column_attrs]

        for param in params:
            column_name = param[0]
            direction = param[1] if len(param) > 1 else 'asc'
            if column_name in mapped_columns:
                column = getattr(self.model_cls, column_name)
                results.append(column.desc() if direction == 'desc' else column)

        return results

    def _serialize_schema_field(self, field):
        result = {
            'label': field.metadata.get('label', None),
            'type': type(field).__name__.lower(),
            'required': field.required,
            'readable': not field.load_only,
            'writable': not field.dump_only,
        }

        if result['type'] == 'nested':
            result['many'] = field.many

        return result
