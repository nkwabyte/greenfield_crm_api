from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Schema endpoint
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger endpoint
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc endpoint
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
