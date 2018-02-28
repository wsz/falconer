from falconer.models import business as model
from falconer.schemas.base import BaseSchema


class StaffSchema(BaseSchema):
    class Meta:
        model = model.Staff


class StoreSchema(BaseSchema):
    class Meta:
        model = model.Store


class PaymentSchema(BaseSchema):
    class Meta:
        model = model.Payment


class RentalSchema(BaseSchema):
    class Meta:
        model = model.Rental
