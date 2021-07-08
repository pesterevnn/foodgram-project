from ..models import Tag


def get_all_tags(request):
    tags = Tag.objects.all()
    return {
        'tags': tags,
    }
