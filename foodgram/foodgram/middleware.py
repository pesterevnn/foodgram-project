from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
