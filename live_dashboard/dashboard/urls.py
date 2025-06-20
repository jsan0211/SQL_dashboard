from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.sample_data, name='data'),
    path('data/gpd/', views.gpd_clients, name='gpd_clients'),
    path('runquery/', views.run_query, name='run_query'),
]

# 👇 Only include this route if DEBUG is True
if settings.DEBUG:
    urlpatterns.append(path('debug/', views.debug_view))