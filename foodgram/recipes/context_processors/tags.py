from ..models import Tags


def get_all_tags(request):
    tags = Tags.objects.all()
    section = request.resolver_match.url_name

    return {
        'tags': tags,
        'section': section,
    }
