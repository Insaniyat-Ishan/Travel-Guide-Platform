# Generated by Django 5.0.2 on 2024-03-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0019_remove_plane_arrival_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plane',
            name='destination_country',
        ),
        migrations.AddField(
            model_name='plane',
            name='arrival_country',
            field=models.CharField(default='Bangladesh', max_length=100),
        ),
        migrations.AddField(
            model_name='plane',
            name='departure_country',
            field=models.CharField(default='India', max_length=100),
        ),
    ]
