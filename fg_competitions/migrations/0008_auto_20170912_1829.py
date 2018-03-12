# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-12 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fg_competitions', '0007_auto_20170818_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedSubmissionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_type', models.CharField(choices=[('T', 'Text Submission'), ('U', 'Upload')], max_length=1)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fg_competitions.Track')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='allowedsubmissiontype',
            unique_together=set([('track', 'submission_type')]),
        ),
    ]
