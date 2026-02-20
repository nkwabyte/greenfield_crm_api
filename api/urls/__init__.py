from django.urls import path, include

urlpatterns = [
    # Admin root
    path('', include('api.urls.admin')),
    
    # Swagger/Redoc endpoints
    path('api/', include('api.urls.docs')),
    
    # API v1 logic endpoints (includes welcome route at /api/v1/)
    path('api/v1/', include('api.urls.api')),
]
