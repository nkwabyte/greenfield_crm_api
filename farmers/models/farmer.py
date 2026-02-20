from django.db import models
from django.utils import timezone
from core.models.base import SoftDeleteTimestampModel
from inventory.models.product import Product

class Farmer(SoftDeleteTimestampModel):
    """
    Core farmer entity mapping to frontend Farmer type.
    """
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    society = models.CharField(max_length=100, null=True, blank=True)
    community = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100, null=True, blank=True)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # acres
    crops_grown = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True) # Active, Inactive
    join_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class FarmerGroup(SoftDeleteTimestampModel):
    """
    Annual segregation group for farmers.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    season_year = models.CharField(max_length=20)
    farmers = models.ManyToManyField(Farmer, related_name='groups', blank=True)

    def __str__(self):
        return f"{self.name} ({self.season_year})"


class FarmerRequest(SoftDeleteTimestampModel):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='requests')
    group = models.ForeignKey(FarmerGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name='requests')
    season_year = models.CharField(max_length=20)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50) # Pending, Approved, Rejected, Delivered
    request_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Request by {self.farmer.name} on {self.request_date}"
