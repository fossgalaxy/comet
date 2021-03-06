# Generated by Django 2.0.2 on 2018-03-09 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fg_competitions', '0010_submission_allow_download'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='allow_download',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submission',
            name='allow_download',
            field=models.BooleanField(default=False, help_text='Allow public distribution after results publication', verbose_name='Make public'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='description',
            field=models.TextField(blank=True, help_text='Briefly describe your submission'),
        ),
    ]
