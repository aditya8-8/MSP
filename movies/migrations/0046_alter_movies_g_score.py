# Generated by Django 5.0.4 on 2024-04-30 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0045_remove_movies_p_score_movies_g_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='g_score',
            field=models.DecimalField(blank=True, decimal_places=20, default=0, max_digits=20, null=True),
        ),
    ]
