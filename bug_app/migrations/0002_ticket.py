# Generated by Django 3.0.6 on 2020-05-21 04:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bug_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('dateFiled', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Done', 'Done'), ('Invalid', 'Invalid')], default='New', max_length=11)),
                ('userAssigned', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_user', to=settings.AUTH_USER_MODEL)),
                ('userCompleted', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completed_user', to=settings.AUTH_USER_MODEL)),
                ('userFiled', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filed_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]