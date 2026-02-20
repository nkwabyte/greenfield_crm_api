from core.views.base import DeltaSyncModelViewSet
from inventory.models import Product, Supplier
from inventory.serializers import ProductSerializer, SupplierSerializer

class ProductViewSet(DeltaSyncModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

class SupplierViewSet(DeltaSyncModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer
