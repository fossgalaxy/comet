# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 00:11
from __future__ import unicode_literals

from django.db import migrations, models
import fg_competitions.models


class Migration(migrations.Migration):

    dependencies = [
        ('fg_competitions', '0002_auto_20160903_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionupload',
            name='status',
            field=models.CharField(choices=[('BP', 'Build pending'), ('BF', 'Build failed'), ('BS', 'Build succeeded'), ('DA', 'Disqualified by admin')], default='BP', max_length=5),
        ),
        migrations.AlterField(
            model_name='submissionupload',
            name='upload',
            field=models.FileField(upload_to=fg_competitions.models.submission_path, validators=[fg_competitions.models.ExtensionValidator(['zip'])]),
        ),
    ]
