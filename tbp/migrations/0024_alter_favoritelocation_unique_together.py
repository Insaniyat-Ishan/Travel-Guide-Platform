# Generated by Django 5.0.3 on 2024-03-29 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0023_alter_favoritehotel_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoritelocation',
            unique_together={('traveler', 'destination')},
        ),
    ]
