from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from business.utils.modelling import ExternalBase
from stocks.models import Stock


class Transaction(ExternalBase):  
    """ Region Model """

    id = models.CharField(
        primary_key=True, 
        null=False,
        blank=False,
        max_length=20,
        verbose_name = "Transaction ID"
    )

    date = models.DateField(
        default=now,
        verbose_name="Transaction Date"
    )

    stock_id = models.ForeignKey(
        Stock,
        blank=True,
        null=True,
        related_name="stock_id",
        on_delete=models.CASCADE,
        verbose_name="Stock ID",
        editable=False
    )

    stock_name = models.ForeignKey(
        Stock,
        blank=True,
        null=True,
        related_name="stock_name",
        on_delete=models.CASCADE,
        verbose_name="Stock Name"
    )

    stock_price = models.PositiveIntegerField(
        null=False, 
        blank=False,
        verbose_name = "Stock Price",
        default=1
    )

    stock_quantity = models.PositiveIntegerField(
        null=False, 
        blank=False,
        verbose_name = "Stock Quantity",
        default=1
    )

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """String representation of the model."""
        return str(self.id)

    class Meta:
        """Meta Data."""

        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
