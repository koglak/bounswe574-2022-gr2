# Generated by Django 4.0.4 on 2022-12-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionlist',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]