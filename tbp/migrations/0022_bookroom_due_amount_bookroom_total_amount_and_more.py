# Generated by Django 5.0.3 on 2024-03-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbp', '0021_destination_faq_favoritehotel_favoritelocation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookroom',
            name='due_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='bookroom',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='bookvehicle',
            name='due_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='bookvehicle',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
