"""
URL configuration for AFK project.

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
from django.urls import path
from main import views as main_views
from authentication import views as auth_views
from profiles import views as profiles_views
from admin_system import views as admin_system_views
from taskGenerator import views as taskGenerator_views

urlpatterns = [
    path("", main_views.main, name="main"),

    path('profile/<int:user_id>/', profiles_views.profile_view, name='profile'),
    path("profile/<int:user_id>/logout/", auth_views.user_profile_logout, name="logout"),

    path('events/', taskGenerator_views.events_view, name='events'),
    path('events/generation/', taskGenerator_views.tasks_idea_generation, name='events/generation'),

    path('forgot_password/', auth_views.forgot_password_view, name='forgot_password'),
    path('forgot_password/submit_form/', auth_views.user_forgot_password_submit, name='forgot_password/submit_form'),

    path("login/", auth_views.login_view, name="login"),
    path('login/yandex/', auth_views.user_yandex_auth, name='login/yandex'),
    path("login/submit_form/", auth_views.user_login_submit, name="login/submit_form"),

    path("register/", auth_views.register_view, name="register"),
    path("register/submit_form/", auth_views.user_register_submit, name="register/submit_form"),

    path("admin/users/", admin_system_views.users_view, name="admin/users"),

    path('profile/setting', profiles_views.setting, name='setting'),

    path("admin/users/add/", admin_system_views.admin_users_add, name="admin/users/add"),
    path("admin/users/edit/", admin_system_views.admin_users_edit, name="admin/users/edit"),
    path("admin/users/delete/", admin_system_views.admin_users_delete, name="admin/users/delete"),

    path("admin/profiles/", admin_system_views.profiles_view, name="admin/profiles"),
    path("admin/profiles/edit/", admin_system_views.admin_profiles_edit, name="admin/profiles/edit"),
    
    path("admin/tasks/", admin_system_views.tasks_view, name="admin/tasks"),
    path("admin/tasks/add/", admin_system_views.admin_tasks_add, name="admin/tasks/add"),
    path("admin/tasks/edit/", admin_system_views.admin_tasks_edit, name="admin/tasks/edit"),
    path("admin/tasks/delete/", admin_system_views.admin_tasks_delete, name="admin/tasks/delete"),

    path("top/", main_views.top, name="top"),
]
