# Generated by Django 3.2.5 on 2022-05-14 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_users', '0007_cartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
