from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),           # for index.html
    path('data/', views.sample_data, name='data')  # for fetch()
]
