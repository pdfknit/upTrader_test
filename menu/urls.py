# menu/urls.py
from django.urls import path
from .views import IndexView  # Импортируйте представления

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]