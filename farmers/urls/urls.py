from rest_framework.routers import DefaultRouter
from farmers.views import FarmerViewSet, FarmerGroupViewSet, FarmerRequestViewSet

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'farmer-groups', FarmerGroupViewSet, basename='farmergroup')
router.register(r'farmer-requests', FarmerRequestViewSet, basename='farmerrequest')

urlpatterns = router.urls
