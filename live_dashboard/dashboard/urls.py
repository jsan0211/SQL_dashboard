from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.sample_data, name='data'),
    path('debug/', views.debug_view, name='debug'),  # 👈 new debug endpoint
]

