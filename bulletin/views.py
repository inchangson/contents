from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, BulletinReply
from .forms import PostForm
from django.utils import timezone
# Create your views here.

def board(request):
    # 게시판 (등록일 기준 최신 순- 작성일 desc)
    posts = Post.objects.all().order_by('-write_date')
    
    # query param 으로 넘어오는 page 값
    current_page      = int(request.GET.get('page', 1))
    
    # 한 페이지 당 5개 피드
    post_count = 5
    paginator  = Paginator(posts, post_count)

    # 최대페이지보다 클 경우 요청 페이지를 마지막 페이지로
    current_page = min(current_page, paginator.num_pages)

    # 출력 범위 설정
    print_range = 5
    start_page = (current_page - 1) // print_range * print_range + 1
    end_page = min(start_page + (print_range - 1), paginator.num_pages)
    
    # 현재 페이지
    post_list = paginator.page(current_page)
    context = {'post_list':post_list,  'current_page' : current_page, 'page_range' : range(start_page, end_page + 1),}

    return render(request, 'bulletin/board.html', context)

def post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    reply_list = BulletinReply.objects.filter(post__id=post_id)
    if request.method == "POST":

        reply   = BulletinReply()
        reply.post = Post.objects.get(id = post_id)
        reply.user         = request.user
        reply.content      = request.POST.get('content')
        reply.created_at   = timezone.now()
        if reply.content != '':
            print(reply.content)
            reply.save()

    return render(request, 'bulletin/post.html', {'post':post, 'reply_list':reply_list})

def upload(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.write_date = timezone.now()
            post.user = request.user
            post.save()   
            return redirect("../")
    elif not request.user.is_authenticated:
        return redirect('/log_sign/login')
    else:
        form = PostForm()

    return render(request, 'bulletin/upload.html', {'form':form})
    
def modify(request, post_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    # post = get_object_or_404(Post, id=post_id)
    post = Post.objects.get(id=post_id)
    

    # if post.author.id != login_session:
    #     return redirect('../bulletin/post_detail/{post_id}/')

    if request.method == "POST":
        form = Post(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()

            post.save()
            return redirect('/bulletin/' + str(post.id), context)
    else:
        form = Post(instance=post)
    
    context = {'form': form}
    return render(request, 'bulletin/post_modify.html', context)


def delete(request, post_id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Post, id=post_id)
    
    context = {'post': post}

    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/bulletin')