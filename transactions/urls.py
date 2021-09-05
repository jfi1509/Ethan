from django.urls import path
from . import views

# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('transactions', views.index, name="transactions"),
    path('add-transaction', views.add_transaction, name="add-transaction"),
    path('edit-transaction/<int:id>', views.edit_transaction, name="edit-transaction"),
    path('delete-transaction/<int:id>', views.delete_transaction, name="delete-transaction"),
]