import base64
import json
import zlib

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, reverse

User = get_user_model()


def sso_login_handler(request, *args, **kwargs):
    try:
        ndoptor_cookie = request.GET.get('data')
        path = request.GET.get('next')
        path = path.split('?')[0]

        sso_status, sso_cookie = unzip_doptor_cookie(request, ndoptor_cookie)
        if sso_status == 'success':
            login_user(request, sso_cookie)
        else:
            return HttpResponseBadRequest()
    except Exception as e:
        return HttpResponseBadRequest()

    return redirect(request.build_absolute_uri(path))


def unzip_doptor_cookie(request, response):
    """
    process sso resposne to python native data type.
    """
    try:
        response_b64_byte = base64.b64decode(response)
        response_json_byte = zlib.decompress(response_b64_byte)
        response_json_string = response_json_byte.decode('utf-8')
        response_dict = json.loads(response_json_string)
        response_status = response_dict.get('status')
        response_status = response_status.strip()

    except Exception as e:
        return HttpResponseBadRequest()
    return response_status, response_dict


def login_user(request, sso_data):
    """
    login user in chat local server.
    """
    try:
        username = sso_data['user_info']['user']['username']
        is_active = sso_data['user_info']['user']['active']
        name_eng = sso_data['user_info']['employee_info']['name_eng']
        name_bng = sso_data['user_info']['employee_info']['name_bng']
        user = authenticate(
            request,
            username=username,
            name_eng=name_eng,
            name_bng=name_bng,
            is_active=is_active,
        )
        request.session['name'] = user.username
        request.session['name_eng'] = user.username_eng
        login(request, user)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def logout_view(request):
    logout(request)

    home_url = request.build_absolute_uri(reverse('home'))
    home_url_b64_byte = base64.b64encode(home_url.encode('utf-8'))
    home_url_b64_string = home_url_b64_byte.decode('utf-8')
    logout_redirect_url = (
        settings.SSO_LOGOUT_URL + "?" + "referer=" + home_url_b64_string
    )

    return redirect(logout_redirect_url)
