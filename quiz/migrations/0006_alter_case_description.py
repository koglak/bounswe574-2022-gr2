# Generated by Django 4.0.4 on 2022-11-26 13:54

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_remove_comment_created_date_alter_comment_dislikes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
