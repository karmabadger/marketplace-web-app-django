from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout/overview/', views.overview, name="overview"),
    path('confirmation', views.confirmation, name="confirmation"),
    path('remove_quantity/<int:id>', views.remove_quantiy, name="remove"),
    path('add_quantity/<int:id>', views.add_quantity, name="add")
]