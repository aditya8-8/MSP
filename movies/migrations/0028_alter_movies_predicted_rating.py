# Generated by Django 5.0.4 on 2024-04-21 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0027_alter_movies_predicted_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='Predicted_Rating',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
