# Generated by Django 3.2.25 on 2025-03-03 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmGenerator', '0010_auto_20250302_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonplayerstats',
            name='overall_rating',
            field=models.IntegerField(default=0),
        ),
    ]
