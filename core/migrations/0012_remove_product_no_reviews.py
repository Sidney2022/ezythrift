# Generated by Django 3.2 on 2023-07-13 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20230713_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='no_reviews',
        ),
    ]