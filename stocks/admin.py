from django.contrib import admin

from stocks.models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name',
        'owner'
    )
    search_fields = (
        'name', 
        'owner'
    )

    list_per_page = 20

admin.site.register(Stock, StockAdmin)
