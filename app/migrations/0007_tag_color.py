# Generated by Django 5.0.3 on 2024-05-27 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_tag_bootstrap_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#dd1111', max_length=10),
        ),
    ]
