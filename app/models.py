from django.db import models
import django.contrib.auth.models


class Tag(models.Model):
    name_id = models.TextField(max_length=20)
    display_name = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    django_user = models.OneToOneField(
        django.contrib.auth.models.User, on_delete=models.CASCADE
    )
    avatar_path = models.FilePathField(max_length=300)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    user_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    title = models.TextField(max_length=200)
    text = models.TextField(max_length=2000)
    image_path = models.FilePathField(max_length=300)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=2000)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VoteToUser(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote"
    )
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_to_who_is_vote"
    )
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "user_to"]]


class VoteToQuestion(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote_to_q"
    )
    question_to = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "question_to"]]


class VoteToAnswer(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_who_vote_to_a"
    )
    answer_to = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = [["user_from", "answer_to"]]
