import collections

import marshmallow_sqlalchemy as ma
from sqlalchemy.orm import ColumnProperty

from falconer.db.model import Base


def _is_primary_key(column):
    return getattr(column, 'primary_key', False)


def _is_filled_by_db(column):
    return getattr(column, 'onupdate', None) is not None


def _is_read_only(column):
    return _is_primary_key(column) or _is_filled_by_db(column)


class BaseModelConverter(ma.ModelConverter):
    def property2field(self, prop, instance=True, field_class=None, **kwargs):
        # add some additional recognition if it is a simple mapping of a property to a single column
        column_property = isinstance(prop, ColumnProperty)
        columns = getattr(prop, 'columns', None)
        column = columns[0] if columns and len(columns) == 1 else None

        if column_property is not None and _is_read_only(column):
            kwargs['dump_only'] = True

        return super(BaseModelConverter, self).property2field(prop, instance, field_class, **kwargs)


class BaseSchemaOpts(ma.ModelSchemaOpts):
    def __init__(self, meta, *args, **kwargs):
        if not hasattr(meta, 'model_converter'):
            meta.model_converter = BaseModelConverter
        super(BaseSchemaOpts, self).__init__(meta, *args, **kwargs)


class BaseSchema(ma.ModelSchema):
    OPTIONS_CLASS = BaseSchemaOpts

    def get_attribute(self, obj, attr, default):
        field = super(BaseSchema, self).get_attribute(obj, attr, default)
        if self.many and isinstance(field, collections.Sequence) and all(isinstance(obj, Base) for obj in field):
            # do not serialize one to many fields when serializing many objects
            return default

        return field
