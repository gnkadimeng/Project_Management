# Generated by Django 5.2 on 2025-06-26 02:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminpanel', '0001_initial'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='assigned_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adminpanelprojects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supervisorfeedback',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_feedback', to='projects.submission'),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='user',
            field=models.OneToOneField(limit_choices_to={'role': 'admin'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='supervisorfeedback',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpanel.supervisorprofile'),
        ),
    ]
