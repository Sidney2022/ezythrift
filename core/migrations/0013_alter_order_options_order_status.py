# Generated by Django 4.1.7 on 2023-07-01 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_order_id_alter_order_tracking_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('canceled', 'Cancelled')], default='in progress', max_length=40),
        ),
    ]
