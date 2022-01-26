from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import BulletinFeed, BulletinReply
from .forms import BulletinFeedForm
from django.utils import timezone
# Create your views here.

def board(request):
    # 게시판 (등록일 기준 최신 순- 작성일 desc)
    feeds = BulletinFeed.objects.all().order_by('-write_date')
    
    # query param 으로 넘어오는 page 값
    current_page      = int(request.GET.get('page', 1))
    
    # 한 페이지 당 5개 피드
    feed_count = 5
    paginator  = Paginator(feeds, feed_count)

    # 최대페이지보다 클 경우 요청 페이지를 마지막 페이지로
    current_page = min(current_page, paginator.num_pages)

    # 출력 범위 설정
    print_range = 5
    start_page = (current_page - 1) // print_range * print_range + 1
    end_page = min(start_page + (print_range - 1), paginator.num_pages)
    
    # 현재 페이지
    board = paginator.page(current_page)
    context = {'board':board,  'board_number' : current_page, 'page_range' : range(start_page, end_page + 1),}

    return render(request, 'bulletin/board.html', context)

def feed(request, feed_id):
    feed = get_object_or_404(BulletinFeed, id = feed_id)
    reply_list = BulletinReply.objects.filter(bulletinfeed__id=feed_id)
    if request.method == "POST":

        reply   = BulletinReply()
        reply.bulletinfeed = BulletinFeed.objects.get(id = feed_id)
        reply.user         = request.user
        reply.content      = request.POST.get('content')
        reply.created_at   = timezone.now()
        if reply.content != '':
            print(reply.content)
            reply.save()

    return render(request, 'bulletin/feed.html', {'feed':feed, 'reply_list':reply_list})

def upload(request):
    if request.method == "POST":
        form = BulletinFeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.write_date = timezone.now()
            feed.user = request.user
            feed.save()   
            return redirect("../")
    elif not request.user.is_authenticated:
        return redirect('/log_sign/login')
    else:
        form = BulletinFeedForm()

    return render(request, 'bulletin/upload.html', {'form':form})
    
def modify(request, post_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    # post = get_object_or_404(Post, author_id=post_id)

    context = {'post': post}

    # if post.author.id != login_session:
    #     return redirect('../freeboard/post_detail/{post_id}/')

    if request.method == 'GET':
        form = PostForm(instance=post)
        context['forms'] = form
        return render(request, 'freeboard/post_modify.html', context)

    elif request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.subject = form.subject
            post.content = form.content
            post.modify_date = timezone.now()

            post.save()
            return redirect('/freeboard')

        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'freeboard/post_modify.html', context)


def delete(request, post_id):
    login_session = request.session.get('login_session', '')
    # post = get_object_or_404(Post, author_id=post_id)
    
    # if post.author.author_id != login_session:
    #     return redirect('../freeboard/post_detail/{post_id}/')
    # else:
    #     post.author.author_id == login_session
    #     post.delete()
    #     return redirect('../freeboard')