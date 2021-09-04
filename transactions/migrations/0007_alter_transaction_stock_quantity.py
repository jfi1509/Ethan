# Generated by Django 3.2 on 2021-09-04 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='stock_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Stock Quantity'),
        ),
    ]
