# Generated by Django 3.2 on 2023-07-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_orderitem_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='unit_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]