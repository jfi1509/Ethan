# Generated by Django 3.2 on 2021-09-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20210904_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Transaction ID'),
        ),
    ]
