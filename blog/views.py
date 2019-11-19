from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def post_list(request):  # request 변수 - 사용자의 웹 주소가 다 넘어가는 변수
    # views.post_list 함수는 이제 DB에서 필요한 데이터를 가져와서
    # post_list.html에게 넘겨줘야 함.
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # 게시일자가 지금보다 이전으로 들어있는 행만 검색 + 최신순으로 정렬
    # render 함수 화면을 그리는 걸 말함(렌더링)
    return render(              # render() 함수를 호출하여 화면을 출력
        request,                # 함수에게 사용자가 요청한 정보를 전달
        'blog/post_list_table.html',  # 화면 출력 주체 지정
        {'posts': posts}        # 화면 출력에 사용할 데이터 전
    )


def homepage(request):
    return render(request, 'blog/homepage.html', {})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# def post_new(request):
#     form = PostForm()  # forms.py 내부의 PostForm 클래스
#     return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()  # 수정 날짜를 따로 하는게 좋을 것 같아
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

