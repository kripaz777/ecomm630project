# Generated by Django 4.0.6 on 2022-08-05 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discounted_price',
            field=models.IntegerField(default=0),
        ),
    ]
