# Generated by Django 3.2 on 2021-09-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_stock_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Stock ID'),
        ),
    ]
