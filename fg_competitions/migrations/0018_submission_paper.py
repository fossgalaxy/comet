# Generated by Django 2.2.6 on 2019-10-24 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fg_competitions', '0017_auto_20190319_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='paper',
            field=models.URLField(blank=True, help_text='Provide a link to your research paper', null=True),
        ),
    ]
