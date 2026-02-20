from core.views.base import DeltaSyncModelViewSet
from finances.models import Transaction
from finances.serializers import TransactionSerializer

class TransactionViewSet(DeltaSyncModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer
