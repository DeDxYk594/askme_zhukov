# Generated by Django 5.0.3 on 2024-05-29 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_avatar_path_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image_path',
            field=models.ImageField(max_length=300, upload_to=''),
        ),
    ]