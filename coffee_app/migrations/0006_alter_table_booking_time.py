# Generated by Django 4.0 on 2022-01-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_app', '0005_table_booking_time_table_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='booking_time',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]