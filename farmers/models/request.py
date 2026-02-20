import uuid
from django.db import models
from farmers.models.farmer import FarmerRequest
from inventory.models.product import Product

class RequestItem(models.Model):
    """
    Items belonging to a FarmerRequest.
    These are purely relational mapping rows and do not require soft-deletes, they are fully replaced
    on edit from the frontend, and deleted physically when removed.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.ForeignKey(FarmerRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255) # Stored redundantly incase product gets deleted
    quantity = models.IntegerField()
    dynamic_price = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
