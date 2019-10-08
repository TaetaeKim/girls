from django.urls import path
from . import views

urlpatterns = [
    # path('url', 사용할 함수 혹은 클래스, 이름)
    path('', views.post_list, name='post_list'),  # 나중에 template에서 view로 접근할 때 사용할 이름 지정
]