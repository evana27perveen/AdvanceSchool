# Generated by Django 3.2.13 on 2022-07-06 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_main', '0009_routinemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice', models.FileField(upload_to='notices')),
                ('created', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice_provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]