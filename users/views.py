# users/settings
import base64
import json
import zlib

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, reverse

User = get_user_model()


def sso_login_handler(request, *args, **kwargs):

    ndoptor_cookie = request.GET.get('data')

    if not ndoptor_cookie:
        redirect_path = request.GET.get('next')
        request.session['redirect_path'] = redirect_path
        login_redirect_url = request.build_absolute_uri(request.path)
        login_redirect_url_b64_byte = base64.b64encode(login_redirect_url.encode('utf-8'))
        login_redirect_url_b64_string = login_redirect_url_b64_byte.decode('utf-8')

        ndoptor_login_url = settings.SSO_LOGIN_URL + "?" + "referer=" + login_redirect_url_b64_string
        return redirect(ndoptor_login_url)

    sso_status, sso_cookie = unzip_doptor_cookie(request, ndoptor_cookie)

    if sso_status == 'success':
        login_user(request, sso_cookie)
    else:
        return HttpResponseBadRequest()

    redirect_path = request.session['redirect_path']

    return redirect(request.build_absolute_uri(redirect_path))


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
    login user in local server.
    """
    try:
        username = sso_data['user_info']['user']['username']
        is_active = sso_data['user_info']['user']['active']
        name_eng = sso_data['user_info']['employee_info']['name_eng']
        name_bng = sso_data['user_info']['employee_info']['name_bng']
        designation = sso_data['user_info']['office_info'][0]['designation']
        office_name_bn = sso_data['user_info']['office_info'][0]['office_name_bn']
        office_name_en = sso_data['user_info']['office_info'][0]['office_name_en']
        user = authenticate(
            request,
            username=username,
            name_eng=name_eng,
            name_bng=name_bng,
            is_active=is_active,
        )
        request.session['name'] = user.username
        request.session['name_eng'] = user.username_eng
        request.session['designation'] = designation
        request.session['office_name_bn'] = office_name_bn
        request.session['office_name_en'] = office_name_en
        login(request, user)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def logout_view(request):
    logout(request)

    home_url = request.build_absolute_uri(reverse('home'))
    home_url_b64_byte = base64.b64encode(home_url.encode('utf-8'))
    home_url_b64_string = home_url_b64_byte.decode('utf-8')
    logout_redirect_url = settings.SSO_LOGOUT_URL + "?" + "referer=" + home_url_b64_string

    return redirect(logout_redirect_url)
