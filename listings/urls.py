from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new, name='new'),
    path('view/<int:id>', views.view, name='view'),
    path('', views.browse, name='listings'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='deletelisting'),
    path('add_to_cart/<str:url>/<int:id>', views.add_to_cart, name="addListing"),
    path('add_to_cart/<str:url>/view/<int:id>', views.add_to_cart_view, name="addView"),
    path('your_store', views.list_your_items, name='yourlistings'),
    path('your_view/<int:id>', views.your_view, name='yourview')
]
