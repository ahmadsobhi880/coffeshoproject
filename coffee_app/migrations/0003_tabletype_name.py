# Generated by Django 4.0 on 2022-01-22 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_app', '0002_coffee_coffeetype_order_orderitem_table_tabletype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabletype',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
