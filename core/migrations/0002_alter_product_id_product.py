# Generated by Django 4.1.7 on 2023-07-06 11:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id_product',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
