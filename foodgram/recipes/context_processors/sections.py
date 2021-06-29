def get_section(request):
    section = request.resolver_match.url_name
    return  {'section': section,}
