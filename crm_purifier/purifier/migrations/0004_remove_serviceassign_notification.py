# Generated by Django 5.0.3 on 2024-03-20 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purifier', '0003_customer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceassign',
            name='notification',
        ),
    ]