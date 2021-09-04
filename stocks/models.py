from django.db import models
from django.contrib.auth.models import User

from business.utils.modelling import ExternalBase


class Stock(ExternalBase):  
    """ Region Model """

    id = models.CharField(
        primary_key=True, 
        null=False,
        blank=False,
        max_length=20,
        verbose_name = "Stock ID"
    )

    name = models.CharField(
        max_length=256, 
        null=False, 
        blank=False,
        unique=True,
        verbose_name = "Stock Name"
    )

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        """String representation of the model."""
        return str(self.name)

    class Meta:
        """Meta Data."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
