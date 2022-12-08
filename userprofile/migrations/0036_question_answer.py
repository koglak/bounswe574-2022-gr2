# Generated by Django 4.0.4 on 2022-12-03 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('userprofile', '0035_alter_event_category_alter_event_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('question', tinymce.models.HTMLField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='space_question', to='userprofile.course')),
                ('dislikes', models.ManyToManyField(related_name='space_question_dislike', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='space_question_like', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', tinymce.models.HTMLField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('dislikes', models.ManyToManyField(related_name='space_question_answer_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='space_question_answer_likes', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space_question_answer', to='userprofile.question')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
