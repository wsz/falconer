import argparse
import csv
from datetime import datetime

from sqlalchemy import Table

from falconer.db.utils import session_scope
from falconer import models
from falconer.models import Film

FILES = {
    'actor': models.Actor,
    'address': models.Address,
    'category': models.Category,
    'city': models.City,
    'country': models.Country,
    'customer': models.Customer,
    'film': models.Film,
    'film_actor': models.film_actor_table,
    'film_category': models.film_category_table,
    'inventory': models.Inventory,
    'language': models.Language,
    'payment': models.Payment,
    'rental': models.Rental,
    'staff': models.Staff,
    'store': models.Store,
}


class Command:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Load data')
        # parser.add_argument()  # TODO: data files paths
        parser.parse_args()

    def _convert_type(self, key, value):
        if key.endswith('_id'):
            try:
                return int(value)
            except ValueError:
                return None
        if key == 'last_update' or key.endswith('_date'):
            try:
                return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        if key == 'rating':
            return Film.MpaaRating(value)

        return value

    def run(self):
        for filename, model in FILES.items():
            print(filename)
            with session_scope() as session, open('data/{}.csv'.format(filename)) as csv_file:
                reader = csv.DictReader(csv_file)

                table = model if isinstance(model, Table) else model.__table__

                session.execute(table.insert(), [
                    {key: self._convert_type(key, value) for key, value in row.items() if key} for row in reader
                ])


if __name__ == '__main__':
    command = Command()
    command.run()
