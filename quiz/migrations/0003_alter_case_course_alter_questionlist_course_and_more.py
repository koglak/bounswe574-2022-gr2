# Generated by Django 4.0.4 on 2022-05-14 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0026_event'),
        ('quiz', '0002_caserating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='case_list', to='userprofile.course'),
        ),
        migrations.AlterField(
            model_name='questionlist',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='question_list', to='userprofile.course'),
        ),
        migrations.AlterField(
            model_name='questionlist',
            name='question_list',
            field=models.ManyToManyField(blank=True, to='quiz.question'),
        ),
    ]
