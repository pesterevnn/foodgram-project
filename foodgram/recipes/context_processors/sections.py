def get_section(request):
    if request.resolver_match:
        section = request.resolver_match.url_name
    else:
        section = 'error'
    return  {'section': section,}
