"""
URL configuration for CreakInterview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from base.views import *
from django.conf.urls.static import static
from CreakInterview import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('ask', get_interview_answer, name='ask'),
]
code_editor_action = [
     path('editor/', code_editor, name='code_editor'),
]
generation = [
     path("generate_code",generate_solidity_code,name="generate_solidity_code"),
     path("compile",compile,name="compile"),
     path("scan",scan,name="scan"),
]


urlpatterns += code_editor_action
urlpatterns += generation

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)