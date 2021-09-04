from django.contrib import admin
from django.urls import (
    path,
    include
)
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('transactions.urls')),
    path('stocks/', include('stocks.urls')),
    path('authentication/', include('authentication.urls')),
]
