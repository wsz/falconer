import enum
from decimal import Decimal

from sqlalchemy import (Column, Enum, Integer, String, DateTime, ForeignKey, Numeric, Text, SmallInteger, Table, func)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from falconer.db.model import Base

__all__ = ['Category', 'Actor', 'Language', 'Inventory', 'Film', 'film_category_table', 'film_actor_table']


film_category_table = Table('film_category', Base.metadata,
                            Column('film_id', Integer, ForeignKey('film.film_id'), primary_key=True),
                            Column('category_id', Integer, ForeignKey('category.category_id'), primary_key=True),
                            Column('last_update', DateTime, server_default=func.now(), onupdate=func.now(),
                                   nullable=False))

film_actor_table = Table('film_actor', Base.metadata,
                         Column('actor_id', Integer, ForeignKey('actor.actor_id'), primary_key=True),
                         Column('film_id', Integer, ForeignKey('film.film_id'), primary_key=True),
                         Column('last_update', DateTime, server_default=func.now(), onupdate=func.now(),
                                nullable=False))


class Category(Base):
    __tablename__ = 'category'

    id = Column('category_id', Integer, primary_key=True)
    name = Column(String(length=25), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    films = relationship('Film', back_populates='categories', secondary=film_category_table)


class Actor(Base):
    __tablename__ = 'actor'

    id = Column('actor_id', Integer, primary_key=True)
    first_name = Column(String(length=45), nullable=False)
    last_name = Column(String(length=45), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    films = relationship('Film', back_populates='actors', secondary=film_actor_table)


class Language(Base):
    __tablename__ = 'language'

    id = Column('language_id', Integer, primary_key=True)
    name = Column(String(length=20), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    films = relationship('Film', back_populates='language', foreign_keys='Film.language_id')
    films_original = relationship('Film', back_populates='original_language', foreign_keys='Film.original_language_id')


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column('inventory_id', Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('film.film_id'), nullable=False)
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    film = relationship('Film', back_populates='inventories')
    store = relationship('Store', back_populates='inventories')
    rentals = relationship('Rental', back_populates='inventory')


class Film(Base):
    __tablename__ = 'film'

    class MpaaRating(enum.Enum):
        G = 'G'
        PG = 'PG'
        PG_13 = 'PG-13'
        R = 'R'
        NC_17 = 'NC-17'

    id = Column('film_id', Integer, primary_key=True)
    title = Column(String(length=255), nullable=False)
    description = Column(Text)
    release_year = Column(SmallInteger)
    language_id = Column(Integer, ForeignKey('language.language_id'), nullable=False)
    original_language_id = Column(Integer, ForeignKey('language.language_id'))
    rental_duration = Column(SmallInteger, default=3, nullable=False)
    rental_rate = Column(Numeric(4, 2), default=Decimal(4.99), nullable=False)
    length = Column(SmallInteger)
    replacement_cost = Column(Numeric(5, 2), default=Decimal(19.99), nullable=False)
    rating = Column(Enum(MpaaRating), default=MpaaRating['G'])
    special_features = Column(String(length=255))  # array as comma separated values
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    language = relationship('Language', back_populates='films', foreign_keys=[language_id])
    original_language = relationship('Language', back_populates='films_original', foreign_keys=[original_language_id])
    categories = relationship('Category', back_populates='films', secondary=film_category_table)
    actors = relationship('Actor', back_populates='films', secondary=film_actor_table)
    inventories = relationship('Inventory', back_populates='film')
