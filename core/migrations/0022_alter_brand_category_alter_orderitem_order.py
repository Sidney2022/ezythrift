# Generated by Django 4.1.7 on 2023-07-03 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_alter_orderitem_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.category"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.order"
            ),
        ),
    ]
