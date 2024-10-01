# Generated by Django 5.0.4 on 2024-04-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0051_alter_genre_g_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='g_score',
            field=models.DecimalField(blank=True, decimal_places=16, max_digits=20, null=True),
        ),
    ]
