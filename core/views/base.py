from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime

class DeltaSyncModelViewSet(viewsets.ModelViewSet):
    """
    Base ModelViewSet that supports Delta Synchronization.
    Returns soft-deleted records when `last_sync` is provided 
    to inform the client state, otherwise hides them.
    Filters out records by `updated_at > last_sync`.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        last_sync = self.request.query_params.get('last_sync', None)

        if last_sync:
            try:
                parsed_time = parse_datetime(last_sync)
                if parsed_time:
                    # Delta Sync: Include deleted records so client can remove them locally
                    return queryset.filter(updated_at__gt=parsed_time)
            except ValueError:
                pass
        
        # Initial Payload: exclude deleted records
        return queryset.filter(is_deleted=False)
