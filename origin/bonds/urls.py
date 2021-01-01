from django.urls import path
from . import views

urlpatterns = [
    path('bonds/', views.Bonds.as_view())
]
