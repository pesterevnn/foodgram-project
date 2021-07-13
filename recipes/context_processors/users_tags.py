from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ..utils import get_actual_users_tags


def get_all_users_tags(request):
    tag_click = request.GET.get('tag')
    if request.user.is_authenticated:    
        users_tags = get_actual_users_tags(request, tag_click)
    else:
        user = get_object_or_404(get_user_model(), username='anonymus')
        users_tags = get_actual_users_tags(request, tag_click, user)
    return {
        'users_tags': users_tags,
    }
