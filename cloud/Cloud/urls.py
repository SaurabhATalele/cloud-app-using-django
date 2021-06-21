"""Cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('MyCloud/', admin.site.urls),
    path('u/',include('mycloud.urls')),
    path('',views.home,name="home_login"),
    path('accounts/login/',views.login,name="home_login"),
    path('signup',views.signup,name='signup'),
    path('login/forgot',views.forgot_pass,name="forgot_pass"),
    path('logout',views.logout,name="logout"),
    # path('changepass',views.changepass,name="new_pass"),
    
    path('<str:username>/<str:password>/',views.loginmanual)
]

handler404 = 'Cloud.views.view_404'
handler500 = 'Cloud.views.view_500'