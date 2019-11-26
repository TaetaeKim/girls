"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from blog import views
# from . import views                           # !!!
# from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.homepage, name='home'),    # views 파일의 homepage라는 함수 호출
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # accounts/가 들어오면 저기로 넘겨라(장고의 accounts 기능을 쓰겠다)
    # django.contrib.auth.urls에 정의되어 있는 urlpattern
    # accounts/login/                     [name='login']
    # accounts/logout/                    [name='logout']
    # accounts/password_change/           [name='password_change']
    # accounts/password_change/done/      [name='password_change_done']
    # accounts/password_reset/            [name='password_reset']
    # accounts/password_reset/done/       [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/    [name='password_reset_confirm']
    # accounts/reset/done/                [name='password_reset_complete']
    path('blog/', include('blog.urls')),
    # path('', include('blog.urls')),  # include = 'blog.urls'가서 알아봐라!

    # path('accounts/login/', views.login, name='login'),
    # path('accounts/logout/', views.logout, name='logout', kwargs={'next_page': '/'}),
    # path('accounts/login/', LoginView.as_view(), name='login'),
    # path('accounts/logout/', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
]
