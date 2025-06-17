from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.sample_data, name='data'),
]

# 👇 Only include this route if DEBUG is True
if settings.DEBUG:
    urlpatterns.append(path('debug/', views.debug_view))