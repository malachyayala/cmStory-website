# Generated by Django 3.2.25 on 2025-03-10 00:39

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardWinner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('club_logo_small_url', models.URLField(blank=True, null=True)),
                ('club_logo_big_url', models.URLField(blank=True, null=True)),
                ('overall', models.IntegerField(help_text="Club's overall rating from 1 to 99", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('att_rating', models.IntegerField(help_text="Club's attack rating from 1 to 99", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('mid_rating', models.IntegerField(help_text="Club's midfield rating from 1 to 99", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('def_rating', models.IntegerField(help_text="Club's defense rating from 1 to 99", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('country', models.CharField(db_index=True, max_length=100)),
                ('scout_region', models.CharField(max_length=100)),
                ('dom_prestige', models.IntegerField(help_text='Domestic prestige from 1 to 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('intl_prestige', models.IntegerField(help_text='International prestige from 1 to 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('league_rep', models.IntegerField(help_text='League reputation from 1 to 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('youth_scouting_region', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Club',
                'verbose_name_plural': 'Clubs',
            },
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('competition_type', models.CharField(choices=[('LEAGUE', 'League'), ('CUP', 'Cup'), ('INTERNATIONAL', 'International')], db_index=True, default='LEAGUE', max_length=50)),
                ('country', models.CharField(db_index=True, max_length=100)),
                ('logo_url', models.URLField(blank=True, null=True)),
                ('league_rep', models.IntegerField(help_text='League reputation from 0 to 5', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('tier', models.IntegerField(help_text='Competition tier from 1 (top) to 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('min_wage_budget', models.DecimalField(decimal_places=2, help_text='Minimum wage budget in euros', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Competition',
                'verbose_name_plural': 'Competitions',
            },
        ),
        migrations.CreateModel(
            name='IndividualAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(unique=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('positions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('GK', 'Goalkeeper'), ('CB', 'Center Back'), ('LB', 'Left Back'), ('RB', 'Right Back'), ('CDM', 'Defensive Midfielder'), ('CM', 'Central Midfielder'), ('CAM', 'Attacking Midfielder'), ('LM', 'Left Midfielder'), ('RM', 'Right Midfielder'), ('LW', 'Left Winger'), ('RW', 'Right Winger'), ('ST', 'Striker'), ('CF', 'Center Forward')], max_length=3), blank=True, null=True, size=3)),
                ('nationality', models.CharField(max_length=100)),
                ('birth_date', models.DateField()),
                ('birth_year', models.IntegerField(blank=True, null=True)),
                ('age', models.IntegerField()),
                ('face_pic_url', models.URLField(blank=True, null=True)),
                ('wage_eur', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wage_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wage_gbp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract_start', models.DateField()),
                ('contract_end', models.DateField()),
                ('contract_loan', models.BooleanField(default=False)),
                ('overall', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('potential', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('last_import_date', models.DateTimeField(auto_now=True)),
                ('import_source', models.CharField(blank=True, max_length=100, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.club')),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
                'ordering': ['-overall', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('season_number', models.PositiveIntegerField(help_text='Sequential number of this season in the story (1, 2, 3, etc.)')),
                ('is_current', models.BooleanField(default=False)),
                ('transfer_budget', models.DecimalField(blank=True, decimal_places=2, help_text='Available transfer budget at start of season', max_digits=12, null=True)),
                ('wage_budget', models.DecimalField(blank=True, decimal_places=2, help_text='Available wage budget at start of season', max_digits=12, null=True)),
                ('league_position', models.PositiveIntegerField(blank=True, help_text='Final or current league position', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['season_number', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Give your story a memorable title', max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('COMPLETED', 'Completed'), ('ABANDONED', 'Abandoned')], default='ACTIVE', max_length=20)),
                ('formation', models.CharField(help_text='Starting formation (e.g., 4-4-2)', max_length=10)),
                ('difficulty', models.CharField(choices=[('BEGINNER', 'Beginner'), ('AMATEUR', 'Amateur'), ('SEMI-PRO', 'Semi-Pro'), ('PROFESSIONAL', 'Professional'), ('WORLD CLASS', 'World Class'), ('LEGENDARY', 'Legendary'), ('ULTIMATE', 'Ultimate')], default='PROFESSIONAL', max_length=20)),
                ('currency', models.CharField(choices=[('EUR', '€ (Euro)'), ('GBP', '£ (British Pound)'), ('USD', '$ (US Dollar)')], default='EUR', max_length=3)),
                ('challenge', models.TextField(help_text='Describe your career mode challenge')),
                ('background', models.TextField(blank=True, help_text='Provide background context for your story')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=True, help_text='Make story visible to other users')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='cmGenerator.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=12)),
                ('fee_currency', models.CharField(default='EUR', max_length=3)),
                ('transfer_date', models.DateField()),
                ('from_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_out', to='cmGenerator.club')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='cmGenerator.season')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='cmGenerator.story')),
                ('to_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_in', to='cmGenerator.club')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='cmGenerator.story'),
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.IntegerField(default=0, help_text="Player's overall rating for this season", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('appearances', models.IntegerField(default=0, help_text='Total number of appearances across all competitions', validators=[django.core.validators.MinValueValidator(0)])),
                ('goals', models.IntegerField(db_index=True, default=0, help_text='Total number of goals scored', validators=[django.core.validators.MinValueValidator(0)])),
                ('assists', models.IntegerField(default=0, help_text='Total number of assists', validators=[django.core.validators.MinValueValidator(0)])),
                ('clean_sheets', models.IntegerField(default=0, help_text='Total number of clean sheets (mainly for goalkeepers)', validators=[django.core.validators.MinValueValidator(0)])),
                ('red_cards', models.IntegerField(default=0, help_text='Number of red cards received', validators=[django.core.validators.MinValueValidator(0)])),
                ('yellow_cards', models.IntegerField(default=0, help_text='Number of yellow cards received', validators=[django.core.validators.MinValueValidator(0)])),
                ('average_rating', models.DecimalField(db_index=True, decimal_places=2, default=0.0, help_text='Average match rating out of 10', max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_stats', to='cmGenerator.season')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_stats', to='cmGenerator.story')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionWinner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.competition')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_winners', to='cmGenerator.season')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_winners', to='cmGenerator.story')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.club')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionPlayerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.IntegerField(default=0, help_text="Player's overall rating in this competition", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('appearances', models.IntegerField(default=0, help_text='Number of appearances in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('goals', models.IntegerField(db_index=True, default=0, help_text='Goals scored in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('assists', models.IntegerField(default=0, help_text='Assists made in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('clean_sheets', models.IntegerField(default=0, help_text='Clean sheets in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('red_cards', models.IntegerField(default=0, help_text='Red cards in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('yellow_cards', models.IntegerField(default=0, help_text='Yellow cards in this competition', validators=[django.core.validators.MinValueValidator(0)])),
                ('average_rating', models.DecimalField(db_index=True, decimal_places=2, default=0.0, help_text='Average match rating in this competition', max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_stats', to='cmGenerator.competition')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_stats', to='cmGenerator.player')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_player_stats', to='cmGenerator.season')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_player_stats', to='cmGenerator.story')),
            ],
        ),
        migrations.AddIndex(
            model_name='competition',
            index=models.Index(fields=['name'], name='cmGenerator_name_2f78ba_idx'),
        ),
        migrations.AddIndex(
            model_name='competition',
            index=models.Index(fields=['country'], name='cmGenerator_country_3893c5_idx'),
        ),
        migrations.AddConstraint(
            model_name='competition',
            constraint=models.UniqueConstraint(condition=models.Q(('competition_type', 'LEAGUE'), ('tier', 1)), fields=('country', 'tier'), name='unique_tier1_league_per_country'),
        ),
        migrations.AddField(
            model_name='club',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.competition'),
        ),
        migrations.AddField(
            model_name='awardwinner',
            name='award',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.individualaward'),
        ),
        migrations.AddField(
            model_name='awardwinner',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmGenerator.player'),
        ),
        migrations.AddField(
            model_name='awardwinner',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='award_winners', to='cmGenerator.season'),
        ),
        migrations.AddField(
            model_name='awardwinner',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='award_winners', to='cmGenerator.story'),
        ),
        migrations.AlterUniqueTogether(
            name='transfer',
            unique_together={('season', 'player', 'from_club', 'to_club')},
        ),
        migrations.AddIndex(
            model_name='story',
            index=models.Index(fields=['user', 'created_at'], name='cmGenerator_user_id_da74e4_idx'),
        ),
        migrations.AddIndex(
            model_name='story',
            index=models.Index(fields=['status', 'is_public'], name='cmGenerator_status_82d300_idx'),
        ),
        migrations.AddIndex(
            model_name='season',
            index=models.Index(fields=['story', 'is_current'], name='cmGenerator_story_i_5f5065_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('story', 'season_number'), ('story', 'name')},
        ),
        migrations.AddIndex(
            model_name='playerstats',
            index=models.Index(fields=['-goals'], name='cmGenerator_goals_0d833e_idx'),
        ),
        migrations.AddIndex(
            model_name='playerstats',
            index=models.Index(fields=['-average_rating'], name='cmGenerator_average_45bf17_idx'),
        ),
        migrations.AddIndex(
            model_name='playerstats',
            index=models.Index(fields=['-assists'], name='cmGenerator_assists_08aefe_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='playerstats',
            unique_together={('season', 'player')},
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['name', 'overall'], name='cmGenerator_name_fd9190_idx'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['club', 'positions'], name='cmGenerator_club_id_8b3f50_idx'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.CheckConstraint(check=models.Q(('potential__gte', django.db.models.expressions.F('overall'))), name='potential_gte_overall'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.CheckConstraint(check=models.Q(('contract_end__gt', django.db.models.expressions.F('contract_start'))), name='contract_end_after_start'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.CheckConstraint(check=models.Q(('wage_eur__gt', 0), ('wage_usd__gt', 0), ('wage_gbp__gt', 0)), name='positive_wages'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('player_id', 'club'), name='unique_player_club_registration'),
        ),
        migrations.AlterUniqueTogether(
            name='competitionwinner',
            unique_together={('season', 'competition')},
        ),
        migrations.AddIndex(
            model_name='competitionplayerstats',
            index=models.Index(fields=['competition', '-goals'], name='cmGenerator_competi_796020_idx'),
        ),
        migrations.AddIndex(
            model_name='competitionplayerstats',
            index=models.Index(fields=['competition', '-average_rating'], name='cmGenerator_competi_c31f55_idx'),
        ),
        migrations.AddIndex(
            model_name='competitionplayerstats',
            index=models.Index(fields=['competition', '-assists'], name='cmGenerator_competi_eab986_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='competitionplayerstats',
            unique_together={('season', 'competition', 'player')},
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['name'], name='cmGenerator_name_4df87f_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['country'], name='cmGenerator_country_737188_idx'),
        ),
        migrations.AddIndex(
            model_name='club',
            index=models.Index(fields=['overall'], name='cmGenerator_overall_46b2b6_idx'),
        ),
        migrations.AddConstraint(
            model_name='club',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='unique_club_name_per_country'),
        ),
        migrations.AddConstraint(
            model_name='awardwinner',
            constraint=models.UniqueConstraint(fields=('season', 'award'), name='unique_season_award'),
        ),
    ]
