from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import user_passes_test

from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from core.components.credentials.privileges import operator_privilege_check, staff_privilege_check, IsOperatorAuthenticated

# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    renderer_classes,
    parser_classes,
    authentication_classes,
    throttle_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication

import colorama, threading
from core import models
# from uptimecheckcore.components.helpers.configurations import is_secretkey_insecure
# from uptimecheckcore.components.helpers import Slack
# from uptimebot.handler import check_domains, check_domain
from . import forms
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from core.handlers import SecurityGroupHandler

User = get_user_model()

@never_cache
@user_passes_test(operator_privilege_check)
def index(request):
    # return render(request, "panel/index.html",
    #               {
    #                   'title': 'Dashboard',
    #                   'flag_show_create_website_button' : True,
    #               })

    ip_address = None
    try:
        ip_address = request.META['HTTP_CF_CONNECTING_IP']  # REMOTE_ADDR
    except:
        ip_address = None

    if not ip_address:
        try:
            ip_address = request.META['HTTP_X_REAL_IP']  # REMOTE_ADDR
        except:
            ip_address = None

    #BotoHelper.add_security_group_with_ip_to_security_group( "8.8.8.8", 'sg-a83703cd' )
    the_security_group = settings.AWS_EC2_SECURITY_GROUP #'sg-a83703cd'

    result_msg = None

    if request.POST:
        form = forms.SecurityGroupForm(request.POST)

        if form.is_valid():
            ip_address_cidr = "%s/%s" % (form.cleaned_data['ip_address'], form.cleaned_data['cidr_block'])
            return_dict = SecurityGroupHandler.add_security_group_with_ip_to_security_group( the_security_group,
                                                                                   ip_address_cidr,
                                                                                   form.cleaned_data['port'],
                                                                                   form.cleaned_data['ip_protocol'] )

            if 'error' in return_dict:
                result_msg = return_dict['error'] #"IP Address Range added."

            if 'flag_success' in return_dict and return_dict['flag_success'] == True:
                result_msg = "IP Address range added."

    else:
        initial_value = { 'port' : '22'}

        if ip_address:
            initial_value['ip_address'] = ip_address

        form = forms.SecurityGroupForm(initial=initial_value)
        result_msg = None

    form.fields['ip_address'].widget.attrs = {'class': 'form-control'}
    form.fields['cidr_block'].widget.attrs = {'class': 'form-control'}
    form.fields['port'].widget.attrs = {'class': 'form-control'}
    form.fields['ip_protocol'].widget.attrs = {'class': 'form-control'}

    security_group_dict = SecurityGroupHandler.describe_security_group( the_security_group )

    return render( request, 'panel/index.html',
                              {
                              'pagetitle': 'Welcome',
                              'frontpage': True,

                                  'form' : form,
                                  'result_msg' : result_msg,

                                  'security_group_description' : security_group_dict['response'],
                                  'the_security_group' : the_security_group,
                              })


@never_cache
@user_passes_test(operator_privilege_check)
def change_password(request):
    the_user = request.user

    return render(request, "panel/users/change_password.html",
                  {
                      'title': f'Change password for {the_user.username}',
                      'operation': "edit",
                      'the_user' : the_user,
                  })

@api_view(['GET', 'POST', ])
# @authentication_classes((JWTAuthentication, SessionAuthentication))
@authentication_classes((SessionAuthentication,))
@permission_classes((IsOperatorAuthenticated,))
def api_users_change_password(request):
    if settings.DEBUG:
        print(request.data)

    f = forms.ChangePasswordForm(request.data)
    if f.is_valid():
        the_user = request.user
        the_user.set_password(f.cleaned_data["new_password"])
        the_user.save()

        return JsonResponse({
            'status' : 'okay',
        })
    else:
        form_errors = {}
        for e in f.errors.items():
            #print(e)
            form_errors[e[0]] = e[1][0]

        return JsonResponse({
            'status': 'error',
            'form_errors': form_errors,
            'error': "Unable to change password",
        })

@never_cache
@user_passes_test(operator_privilege_check)
def logout_(request):
    logout(request)

    return HttpResponseRedirect("/")  # reverse("landing:index")
