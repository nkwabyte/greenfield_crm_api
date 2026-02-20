from django.urls import path, include
from api.views.welcome import home_api_view

urlpatterns = [
    path('', home_api_view, name='home'),
    path('accounts/', include('accounts.urls.urls')),
    path('farmers/', include('farmers.urls.urls')),
    path('inventory/', include('inventory.urls.urls')),
    path('finances/', include('finances.urls.urls')),
]
