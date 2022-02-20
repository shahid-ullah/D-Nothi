# users/middleware.py
import base64

from django.conf import settings
from django.shortcuts import redirect


def sso_middleware(get_response):
    def middleware(request):
        ndoptor_cookie = not request.GET.get('data')

        if request.user.is_anonymous and ndoptor_cookie:
            login_redirect_url = request.build_absolute_uri()
            login_redirect_url_b64_byte = base64.b64encode(
                login_redirect_url.encode('utf-8')
            )
            login_redirect_url_b64_string = login_redirect_url_b64_byte.decode('utf-8')

            ndoptor_login_url = (
                settings.SSO_LOGIN_URL
                + "?"
                + "referer="
                + login_redirect_url_b64_string
            )
            return redirect(ndoptor_login_url)

        response = get_response(request)

        return response

    return middleware
