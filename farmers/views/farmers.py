from core.views.base import DeltaSyncModelViewSet
from farmers.models import Farmer, FarmerGroup, FarmerRequest
from farmers.serializers import FarmerSerializer, FarmerGroupSerializer, FarmerRequestSerializer

class FarmerViewSet(DeltaSyncModelViewSet):
    queryset = Farmer.objects.all().order_by('-created_at')
    serializer_class = FarmerSerializer

class FarmerGroupViewSet(DeltaSyncModelViewSet):
    queryset = FarmerGroup.objects.all().order_by('-created_at')
    serializer_class = FarmerGroupSerializer

class FarmerRequestViewSet(DeltaSyncModelViewSet):
    queryset = FarmerRequest.objects.all().order_by('-request_date')
    serializer_class = FarmerRequestSerializer
