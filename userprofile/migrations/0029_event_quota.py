# Generated by Django 4.0.4 on 2022-10-24 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0028_event_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='quota',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
