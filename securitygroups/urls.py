"""
URL configuration for securitygroups project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
import os

urlpatterns = [
    path('', include('website.urls')),
    path('panel/', include('panel.urls')),

    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='panel/login.html', extra_context={
        'NAVBAR_STYLE': 'navbar-white'
    }), name="account_login"),

]
if settings.DEBUG:
    from django.conf.urls.static import static

    # urlpatterns += static('media/', document_root=os.path.join(settings.BASE_DIR, 'src/media'))
    urlpatterns += static('lookandfeel/', document_root=os.path.join(settings.BASE_DIR, 'src/lookandfeel/'))
    urlpatterns += static('static/', document_root=os.path.join(settings.BASE_DIR, 'src/static/'))

admin.site.site_header = "Security Groups Webstack by Pulsely"
admin.site.index_title = "Admin Console"
admin.site.site_title = "Security Groups Webstack by Pulsely"
