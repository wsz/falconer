from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean, func)
from sqlalchemy.orm import relationship

from falconer.db.model import Base

__all__ = ['Country', 'City', 'Address', 'Customer']


class Country(Base):
    __tablename__ = 'country'

    id = Column('country_id', Integer, primary_key=True)
    name = Column('country', String(length=50), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    cities = relationship('City', back_populates='country')


class City(Base):
    __tablename__ = 'city'

    id = Column('city_id', Integer, primary_key=True)
    name = Column('city', String(length=50), nullable=False)
    country_id = Column(Integer, ForeignKey('country.country_id'), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    country = relationship('Country', back_populates='cities')
    addresses = relationship('Address', back_populates='city')


class Address(Base):
    __tablename__ = 'address'

    id = Column('address_id', Integer, primary_key=True)
    first_line = Column('address', String(length=50), nullable=False)
    second_line = Column('address2', String(length=50))
    district = Column(String(length=20), nullable=False)
    city_id = Column(Integer, ForeignKey('city.city_id'), nullable=False)
    postal_code = Column(String(length=10))
    phone = Column(String(length=20), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    city = relationship('City', back_populates='addresses')
    customers = relationship('Customer', back_populates='address')
    staff = relationship('Staff', back_populates='address')
    stores = relationship('Store', back_populates='address')


class Customer(Base):
    __tablename__ = 'customer'

    id = Column('customer_id', Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    first_name = Column(String(length=45), nullable=False)
    last_name = Column(String(length=45), nullable=False)
    email = Column(String(length=50))
    address_id = Column(Integer, ForeignKey('address.address_id'), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    create_date = Column(DateTime, server_default=func.now())
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    store = relationship('Store', back_populates='customers')
    address = relationship('Address', back_populates='customers')
    payments = relationship('Payment', back_populates='customer')
    rentals = relationship('Rental', back_populates='customer')
