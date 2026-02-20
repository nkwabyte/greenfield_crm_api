from rest_framework.routers import DefaultRouter
from accounts.views import EmployeeProfileViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeProfileViewSet, basename='employee')

urlpatterns = router.urls
