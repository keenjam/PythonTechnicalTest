from django.urls import path
from . import views

urlpatterns = [
    path('bonds/', views.Bonds.as_view())
    #path('bonds/<str:isin>', views.Bonds.bondData)
]
