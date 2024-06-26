# Generated by Django 5.0.3 on 2024-04-17 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('title', models.TextField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_path', models.TextField(max_length=300)),
                ('rating_likes', models.BigIntegerField(default=0)),
                ('rating_dislikes', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('text', models.TextField(max_length=2000)),
                ('image_path', models.TextField(max_length=300)),
                ('rating_likes', models.BigIntegerField(default=0)),
                ('rating_dislikes', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.ManyToManyField(to='app.tag')),
                ('user_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000)),
                ('rating_likes', models.BigIntegerField(default=0)),
                ('rating_dislikes', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('user_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='VoteToAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_vote_to_a', to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='VoteToQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_vote_to_q', to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='VoteToUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_who_vote', to='app.user')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_who_is_vote', to='app.user')),
            ],
        ),
    ]
