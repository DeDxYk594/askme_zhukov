# Generated by Django 5.0.3 on 2024-05-27 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_tag_rating_questions_user_rating_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='bootstrap_icon',
            field=models.SlugField(default='telephone-plus', max_length=30),
            preserve_default=False,
        ),
    ]