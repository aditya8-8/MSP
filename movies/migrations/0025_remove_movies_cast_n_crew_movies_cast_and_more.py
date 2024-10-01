# Generated by Django 5.0.4 on 2024-04-18 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0024_rename_ph_credit_movies_total_cscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='Cast_n_Crew',
        ),
        migrations.AddField(
            model_name='movies',
            name='cast',
            field=models.ManyToManyField(blank=True, related_name='movie_cast', to='movies.cast_n_crew'),
        ),
        migrations.RemoveField(
            model_name='movies',
            name='director',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='producer',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='writer',
        ),
        migrations.AddField(
            model_name='movies',
            name='director',
            field=models.ManyToManyField(blank=True, related_name='movies_directed', to='movies.cast_n_crew'),
        ),
        migrations.AddField(
            model_name='movies',
            name='producer',
            field=models.ManyToManyField(blank=True, related_name='movies_produced', to='movies.cast_n_crew'),
        ),
        migrations.AddField(
            model_name='movies',
            name='writer',
            field=models.ManyToManyField(blank=True, related_name='movies_written', to='movies.cast_n_crew'),
        ),
    ]
