"""
URL configuration for finance_qa_neo4j project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import RedirectView


def index(request):
    return render(request,'django_qa.html')

from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('', RedirectView.as_view(url='/qa/', permanent=False), name='home'),
    # path("qa/", include("qa_system.urls")),
    # path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('', RedirectView.as_view(url='/qa/', permanent=False), name='home'),
    path("qa/", include("qa_system.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
