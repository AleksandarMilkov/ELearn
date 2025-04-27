"""
URL configuration for eLearnApp project.

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
from django.contrib import admin
from django.urls import path
from eLearnApp.views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import *
from . import views

urlpatterns = [
    path('', views.frontend, name='frontend'),
    path('admin/', admin.site.urls),
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('', home_view, name='home'),
    path("courses/", course_list_view, name="course_list"),
    path("courses/create/", create_course_view, name="create_course"),
    path("courses/<int:course_id>/", course_detail_view, name="course_detail"),
    path("courses/<int:course_id>/lessons/", lesson_list_view, name="lesson_list"),
    path("courses/<int:course_id>/lessons/create/", create_lesson_view, name="create_lesson"),
    path('lessons/<int:lesson_id>/quiz/', quiz_view, name='quiz'),
    path('dashboard/', dashboard_view, name='dashboard'),

]
