# Generated by Django 4.0.2 on 2022-02-07 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerApp', '0002_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customerId',
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
    ]
