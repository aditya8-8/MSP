# Generated by Django 5.0.4 on 2024-04-07 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_movies_yt_trailer_dislike_alter_movies_imdb_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='imdb_meta',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
