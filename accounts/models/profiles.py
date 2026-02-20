from django.db import models
from core.models.base import SoftDeleteTimestampModel
from accounts.models.user import User

class EmployeeProfile(SoftDeleteTimestampModel):
    """
    Represents the business data for an employee, linking to the User for auth.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    role_title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    status = models.CharField(max_length=50) # Active, On Leave, Terminated
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
