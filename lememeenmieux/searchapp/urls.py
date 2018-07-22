"""lememeenmieux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name='index'),
    url(r'^product/', views.product, name='product'),
    url(r'^results/', views.results, name='results'),
    url(r'^myaccount/', views.myaccount, name='myaccount'),
    url(r'^login/', views.dologin, name='dologin'),
    url(r'^logout/', views.dologout, name='dologout'),
    url(r'^legalnotice/', views.legalnotice, name='legalnotice'),

    #url(r'^$', views.index),

    #url(r'^searchapp/', include('searchapp.urls')), --> NEVER !!!
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns