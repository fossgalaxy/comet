# Generated by Django 2.0.2 on 2018-06-28 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fg_competitions', '0013_auto_20180312_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='allow_sub_text',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='track',
            name='allow_sub_uploads',
            field=models.BooleanField(default=True),
        ),
    ]
