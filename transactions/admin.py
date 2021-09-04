from django.contrib import admin

from transactions.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stock_name',
        'stock_price',
        'stock_quantity',
        'owner'
    )
    search_fields = (
        'id',
        'stock_name',
        'stock_price',
        'owner'
    )

    exclude = ('stock_id',)

    list_per_page = 20

admin.site.register(Transaction, TransactionAdmin)


