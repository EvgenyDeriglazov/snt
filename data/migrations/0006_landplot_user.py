# Generated by Django 3.0.2 on 2020-02-04 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0005_auto_20200123_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='landplot',
            name='user',
            field=models.ForeignKey(blank=True, help_text='аккаунт', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
