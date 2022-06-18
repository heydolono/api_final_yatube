# Generated by Django 4.0.5 on 2022-06-18 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20220618_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='following',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
