# Generated by Django 5.0.3 on 2024-05-29 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_user_avatar_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='avatar_path',
            new_name='avatar',
        ),
    ]