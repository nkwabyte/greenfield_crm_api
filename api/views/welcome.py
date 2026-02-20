from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(
    summary="Home API Endpoint",
    description="Returns a welcome message for the API.",
    responses={200: {"description": "Welcome message"}}
)
def home_api_view(request, *args, **kwargs):
    return Response(
        {
            "message": "Welcome to the Greenfield CRM Project API",
            "status": "success",
            "code": status.HTTP_200_OK,
            "data": {
                "message": "Welcome to the Greenfield CRM Project API",
                "status": "success",
            },
        },
        status=status.HTTP_200_OK,
    )
