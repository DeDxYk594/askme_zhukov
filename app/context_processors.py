from .models import Tag, User


def top_data(request):
    popular_tags = Tag.objects.tops()[:10]
    best_members = User.objects.bests()[:10]

    return {
        "popular_tags": popular_tags,
        "best_members": best_members,
    }
