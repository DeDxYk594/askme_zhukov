from .models import Tag, User
from django.core.cache import cache
from .utils import updateCache
import time

flag = False


def top_data(request):
    global flag
    popular_tags = cache.get("popular_tags")
    best_members = cache.get("popular_users")
    if popular_tags is None:
        if not flag:
            flag = True
            updateCache()
            flag = False
        while flag:
            time.sleep(1)
        popular_tags = cache.get("popular_tags")
        best_members = cache.get("popular_users")
    if not request.user.is_anonymous:
        my_user = User.objects.get(django_user=request.user)
    else:
        my_user = None

    return {
        "popular_tags": popular_tags,
        "best_members": best_members,
        "my_user": my_user,
    }
