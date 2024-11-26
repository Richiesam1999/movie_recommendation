from django.urls import path
from . import views

urlpatterns = [
    path('recommend/<int:id>/', views.recommend, name='recommend'),
]

