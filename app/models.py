from django.db import models
import django.contrib.auth.models


class TagManager(models.Manager):
    def with_question_count(self):
        return self.annotate(question_count=models.Count("question")).order_by(
            "-question_count"
        )


class UserManager(models.Manager):
    def with_rating(self):
        return self.annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(user_to_who_is_vote__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(user_to_who_is_vote__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        )


# Добавить запрос на получение самых новых, самых популярных, сделать вопросы по тегу
class QuestionManager(models.Manager):
    def with_num_answers_and_rating(self):
        return self.annotate(
            answers_count=models.Count("answer"),
        ).annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        )
    
    def hots(self):
        return self.with_num_answers_and_rating().order_by('-(likes_count+dislikes_count)')

    def one_with_rating(self, pk):
        return self.annotate(
            likes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=True, then=1),
                    output_field=models.IntegerField(),
                )
            ),
            dislikes_count=models.Count(
                models.Case(
                    models.When(votetoquestion__is_like=False, then=1),
                    output_field=models.IntegerField(),
                )
            ),
        ).get(pk=pk)


class AnswerManager(models.Manager):
    def answers_for_question(self, question):
        return (
            self.filter(question_to=question)
            .annotate(
                likes_count=models.Count(
                    models.Case(
                        models.When(votetoanswer__is_like=True, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
                dislikes_count=models.Count(
                    models.Case(
                        models.When(votetoanswer__is_like=False, then=1),
                        output_field=models.IntegerField(),
                    )
                ),
            )
            .order_by("-likes_count")
        )


class Tag(models.Model):
    objects = TagManager()
    slug = models.TextField(max_length=20)
    display_name = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    objects = UserManager()
    django_user = models.OneToOneField(
        django.contrib.auth.models.User, on_delete=models.CASCADE
    )
    avatar_path = models.TextField(max_length=300)
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.django_user.username


class Question(models.Model):
    objects = QuestionManager()
    user_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, null=True)
    title = models.TextField(max_length=200)
    text = models.TextField(max_length=2000)
    image_path = models.TextField(max_length=300)  # TODO Сделать ImageField
    rating_likes = models.BigIntegerField(default=0)
    rating_dislikes = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()
    question_to = models.ForeignKey(Question, on_delete=models.CASCADE)
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
