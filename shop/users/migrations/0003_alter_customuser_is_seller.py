# Generated by Django 4.0 on 2021-12-25 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_is_seller_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_seller',
            field=models.BooleanField(default=False, help_text='Does the user have a Shop?'),
        ),
    ]
