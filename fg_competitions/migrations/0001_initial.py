# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-03 17:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompetitionLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fg_competitions.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ranking', models.FloatField(default=1500)),
                ('ranking_rd', models.FloatField(default=350)),
                ('velocity', models.FloatField(default=0.06)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['ranking', 'ranking_rd'],
            },
        ),
        migrations.CreateModel(
            name='SubmissionUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('BP', 'Build pending'), ('BF', 'Build failed'), ('BS', 'Build succeeded')], default='BP', max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(upload_to=b'')),
                ('feedback', models.TextField(blank=True, null=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='fg_competitions.Submission')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('allow_submit', models.BooleanField(default=True)),
                ('allow_update', models.BooleanField(default=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fg_competitions.Competition')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fg_competitions.Track'),
        ),
        migrations.AlterUniqueTogether(
            name='submission',
            unique_together=set([('owner', 'track')]),
        ),
    ]
