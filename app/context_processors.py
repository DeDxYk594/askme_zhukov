from .models import Tag, User


def top_data(request):
    popular_tags = Tag.objects.tops()[:10]
    best_members = User.objects.bests()[:10]
    if not request.user.is_anonymous:
        my_user = User.objects.get(django_user=request.user)
    else:
        my_user = None

    return {
        "popular_tags": popular_tags,
        "best_members": best_members,
        "my_user": my_user,
    }
