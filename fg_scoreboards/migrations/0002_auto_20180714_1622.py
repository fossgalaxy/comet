# Generated by Django 2.0.2 on 2018-07-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fg_scoreboards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreboard',
            name='points_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='scoreboard',
            name='scoring_system',
            field=models.CharField(choices=[('win', 'Total Wins'), ('avg', 'Mean Points'), ('sum', 'Total Points')], default='avg', max_length=3),
        ),
    ]
