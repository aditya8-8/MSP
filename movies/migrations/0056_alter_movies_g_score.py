# Generated by Django 5.0.4 on 2024-04-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0055_alter_movies_v_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='g_score',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3),
        ),
    ]
