"""marketplace URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core import views as core_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

from django.conf.urls import url
# from core import views



urlpatterns = [
    path('accounts/signup/', core_views.signup, name='signup'),
    path('accounts/reset/', core_views.reset_form, name='reset'),
    path('accounts/myaccount/', core_views.myaccount, name='myaccount'),
    path('accounts/reset_request/', core_views.reset_request, name='reset_request'),
    path('accounts/resetconfirmed/', core_views.resetconfirmed, name='resetconfirmed'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('admin/', admin.site.urls, name='admin'),
    path('listings/', include('listings.urls')),
    path('chat/', include('chat.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.resetpass, name='reset'),
    path('', RedirectView.as_view(url='/listings'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)