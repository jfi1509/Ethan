from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="stocks"),
    path('add-stock', views.add_stock, name="add-stock"),
    path('edit-stock/<int:id>', views.edit_stock, name="edit-stock"),
    path('delete-stock/<int:id>', views.delete_stock, name="delete-stock"),
]
