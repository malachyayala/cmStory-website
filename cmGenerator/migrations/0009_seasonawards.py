# Generated by Django 3.2.16 on 2025-03-02 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmGenerator', '0008_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonAwards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=10)),
                ('la_liga_winner', models.CharField(blank=True, max_length=100)),
                ('serie_a_winner', models.CharField(blank=True, max_length=100)),
                ('bundesliga_winner', models.CharField(blank=True, max_length=100)),
                ('ligue_1_winner', models.CharField(blank=True, max_length=100)),
                ('premier_league_winner', models.CharField(blank=True, max_length=100)),
                ('balon_dor_winner', models.CharField(blank=True, max_length=100)),
                ('golden_boy_winner', models.CharField(blank=True, max_length=100)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_awards', to='cmGenerator.story')),
            ],
            options={
                'ordering': ['season'],
                'unique_together': {('story', 'season')},
            },
        ),
    ]
