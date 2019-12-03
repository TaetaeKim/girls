from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate, login, logout


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


@login_required
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


@login_required
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


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    # 원글 post 획득
    # 		만일 요청이 'POST'이면:
    # 			댓글 폼 form을 request.POST로 채워서 생성
    # 			만일 form 정당하면:  # 모델에 정의되어 있는대로 판단
    # 				form을 댓글 comment로 저장
    # 				댓글의 원글 post 획득
    # 				댓글 저장
    # 				게시글 상세 보기 화면으로 리다이렉트하고 종료
    # 		아니면:
    # 			빈 폼 form 생성
    # 		댓글 작성 화면으로 이동
    post = get_object_or_404(Post, pk=pk)  # 찾아오던가 404 에러를 내던가
    if request.method == "POST":  #
        form = CommentForm(request.POST)  # 사용자가 입력한 값으로 내용을 채워서 폼 생성
        if form.is_valid():
            comment = form.save(commit=False)  # 메인메모리에서만 저장(실제 저장 False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()  # 클래스 생성자 사용
    return render(request,  # 전달 받은 것 그대로 전달
                  'blog/add_comment_to_post.html',  # 이 파일 이용해서 그려라
                  {'form': form})  # 이거 가지고 가서!


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


