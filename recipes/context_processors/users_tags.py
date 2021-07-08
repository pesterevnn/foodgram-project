from ..utils import get_actual_users_tags


def get_all_users_tags(request):
    if request.user.is_authenticated:
        tag_click = request.GET.get('tag')
        users_tags = get_actual_users_tags(request, tag_click)
    else:
        users_tags = []
    return {
        'users_tags': users_tags,
    }
