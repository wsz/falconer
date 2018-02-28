from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, func)
from sqlalchemy.orm import relationship

from falconer.db.model import Base

__all__ = ['Staff', 'Store', 'Payment', 'Rental']


class Staff(Base):
    __tablename__ = 'staff'

    id = Column('staff_id', Integer, primary_key=True)
    first_name = Column(String(length=45), nullable=False)
    last_name = Column(String(length=45), nullable=False)
    address_id = Column(Integer, ForeignKey('address.address_id'))
    picture = Column(String(length=200))
    email = Column(String(length=50))
    store_id = Column(Integer, ForeignKey('store.store_id'), nullable=False)
    active = Column(Boolean, nullable=False)
    username = Column(String(length=16), nullable=False)
    password = Column(String(length=40))
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    address = relationship('Address', back_populates='staff')
    store = relationship('Store', back_populates='staff', foreign_keys=[store_id])
    managed_stores = relationship('Store', back_populates='manager_staff', foreign_keys='Store.manager_staff_id')
    payments = relationship('Payment', back_populates='staff')
    rentals = relationship('Rental', back_populates='staff')


class Store(Base):
    __tablename__ = 'store'

    id = Column('store_id', Integer, primary_key=True)
    manager_staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    address_id = Column(Integer, ForeignKey('address.address_id'), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    manager_staff = relationship('Staff', back_populates='managed_stores', foreign_keys=[manager_staff_id])
    staff = relationship('Staff', back_populates='store', foreign_keys='Staff.store_id')
    address = relationship('Address', back_populates='stores')
    customers = relationship('Customer', back_populates='store')
    inventories = relationship('Inventory', back_populates='store')


class Payment(Base):
    __tablename__ = 'payment'

    id = Column('payment_id', Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rental.rental_id'))
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship('Customer', back_populates='payments')
    staff = relationship('Staff', back_populates='payments')
    rental = relationship('Rental', back_populates='payments')


class Rental(Base):
    __tablename__ = 'rental'

    id = Column('rental_id', Integer, primary_key=True)
    rental_date = Column(DateTime, nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    return_date = Column(DateTime)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'), nullable=False)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    inventory = relationship('Inventory', back_populates='rentals')
    customer = relationship('Customer', back_populates='rentals')
    staff = relationship('Staff', back_populates='rentals')
    payments = relationship('Payment', back_populates='rental')
