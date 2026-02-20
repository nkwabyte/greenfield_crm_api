from django.db import models
from core.models.base import SoftDeleteTimestampModel

class Transaction(SoftDeleteTimestampModel):
    type = models.CharField(max_length=50) # Income, Expense
    category = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    employee_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.date})"
