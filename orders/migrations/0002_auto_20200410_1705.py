# Generated by Django 2.0.3 on 2020-04-10 22:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='orders',
            new_name='User_order',
        ),
        migrations.RenameField(
            model_name='user_order',
            old_name='order',
            new_name='order_number',
        ),
    ]
