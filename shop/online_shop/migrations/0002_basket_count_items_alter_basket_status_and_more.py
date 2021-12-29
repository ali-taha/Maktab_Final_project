# Generated by Django 4.0 on 2021-12-29 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='count_items',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('rev', 'Review mode'), ('con', 'Confirmed mode'), ('del', 'Deleted mode')], default='rev', max_length=3),
        ),
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.CharField(choices=[('rev', 'Review mode'), ('con', 'Confirmed mode'), ('del', 'Deleted mode')], default='rev', max_length=3),
        ),
    ]