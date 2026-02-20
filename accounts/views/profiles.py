from core.views.base import DeltaSyncModelViewSet
from accounts.models import EmployeeProfile
from accounts.serializers import EmployeeProfileSerializer

class EmployeeProfileViewSet(DeltaSyncModelViewSet):
    """
    Delta Sync viewset for backend employee data (auth + employee profile).
    """
    queryset = EmployeeProfile.objects.all().order_by('-created_at')
    serializer_class = EmployeeProfileSerializer
