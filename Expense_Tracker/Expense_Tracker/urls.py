"""
URL configuration for Expense_Tracker project.

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
from register import views as v #to distinguish the views of main and register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('', include("django.contrib.auth.urls")),
    path('signup/', v.signup, name='signup'),
    path('login/', v.user_login, name='login'),
    path('user_logout/', v.LogoutView.as_view(), name='logout'),
    path('user_profile/', v.ProfileView.as_view(), name='user_profile'),
    path('update_profile/', v.CustomUserUpdateView.as_view(), name='update_profile'),
    path('delete_account/', v.DeleteAccountView.as_view(), name='delete_account'),

]
