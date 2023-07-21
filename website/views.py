import uuid

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, HttpResponseForbidden
import colorama, random, string, datetime
from django.utils import timezone
from . import forms
from django.contrib.auth import login, logout

# from jobhuntingcore.components.credentials.privileges import employer_privilege_check, jobseeker_privilege_check, \
#     user_privilege_check, staff_privilege_check
from core import models
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
#from . import handler
from django.core.paginator import Paginator

User = get_user_model()

@never_cache
def index(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect( reverse( settings.URL_POST_SIGNIN ))

    return render(request, "website/index.html",
                  {
                      'flag_navbar_transparent': True,
                      'flag_category_home': True,

                  })