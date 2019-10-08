from django.shortcuts import render

# Create your views here.


def post_list(request):  # request 변수 - 사용자의 웹 주소가 다 넘어가는 변수
    return render(request, 'blog/post_list.html', {})  # render 함수 화면을 그리는 걸 말함(렌더링)
