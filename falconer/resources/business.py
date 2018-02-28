from falconer.models.business import Staff, Store, Payment, Rental
from falconer.resources.base import BaseResource
from falconer.schemas.business import StaffSchema, StoreSchema, PaymentSchema, RentalSchema


class StaffResource(BaseResource):
    schema_cls = StaffSchema
    model_cls = Staff
    singular = 'Staff'
    plural = 'Staff'


class StoreResource(BaseResource):
    schema_cls = StoreSchema
    model_cls = Store
    singular = 'Store'
    plural = 'Stores'


class PaymentResource(BaseResource):
    schema_cls = PaymentSchema
    model_cls = Payment
    singular = 'Payment'
    plural = 'Payments'


class RentalResource(BaseResource):
    schema_cls = RentalSchema
    model_cls = Rental
    singular = 'Rental'
    plural = 'Rentals'
