# Generated by Django 5.0.4 on 2024-04-23 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0034_alter_movies_predicted_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='g_score',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=5),
        ),
    ]
