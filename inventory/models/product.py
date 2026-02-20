from django.db import models
from core.models.base import SoftDeleteTimestampModel

class Supplier(SoftDeleteTimestampModel):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(SoftDeleteTimestampModel):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100) # Seeds, Fertilizers, Pesticides, Equipment, Other
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2) # per unit

    def __str__(self):
        return self.name
