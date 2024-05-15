from app.models import (
    Question,
    Answer,
    Tag,
    User,
    VoteToAnswer,
    VoteToQuestion,
    VoteToUser,
)
from django.db.models import Case, IntegerField, When, Count
from tqdm import tqdm


def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def chunks(lst, n=1000):
    return list(_chunks(lst, n))


def recalculateRating():
    print("Recalculating users ratings...")

    calculated_users = User.objects.normalized_rating()
    for user in tqdm(calculated_users):
        user.rating_likes = user.likes_count
        user.rating_dislikes = user.dislikes_count
        user.rating_questions = user.questions_count
        user.rating_answers = user.answers_count

    print("Loading user rating into database..")

    for chunk in tqdm(chunks(calculated_users)):
        User.objects.bulk_update(
            chunk,
            ["rating_likes", "rating_dislikes", "rating_questions", "rating_answers"],
        )

    print("Recalculating questions ratings...")

    calculated_questions = Question.objects.normalized_rating()
    for question in tqdm(calculated_questions):
        question.rating_likes = question.likes_count
        question.rating_dislikes = question.dislikes_count
        question.rating_answers = question.answers_count

    print("Loading question rating into database..")

    for chunk in tqdm(chunks(calculated_questions)):
        Question.objects.bulk_update(
            chunk, ["rating_likes", "rating_dislikes", "rating_answers"]
        )

    print("Recalculating answers ratings...")

    calculated_answers = Answer.objects.normalized_rating()
    for answer in tqdm(calculated_answers):
        answer.rating_likes = answer.likes_count
        answer.rating_dislikes = answer.dislikes_count

    print("Loading answer rating into database..")

    for chunk in tqdm(chunks(calculated_answers)):
        Answer.objects.bulk_update(chunk, ["rating_likes", "rating_dislikes"])

    print("Recalculating tags ratings...")

    calculated_tags = Tag.objects.normalized_rating()
    for tag in tqdm(calculated_tags):
        tag.rating_questions = tag.question_count

    print("Loading tag rating into database..")

    for chunk in tqdm(chunks(calculated_tags)):
        Tag.objects.bulk_update(chunk, ["rating_questions"])
