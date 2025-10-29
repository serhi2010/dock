from django.urls import path
from . import views

app_name = 'advertisement'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('create/', views.advertisement_create, name='advertisement_create'),
    path('<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
]
