from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import BulletinFeed, BulletinReply
from .forms import BulletinFeedForm
from django.utils import timezone
from log_sign.models import User 
# Create your views here.

def board(request):
    # 게시판 (등록일 기준 최신 순- id desc)
    feeds = BulletinFeed.objects.all().order_by('-id')
    # query param 으로 넘어오는 page 값
    current_page = int(request.GET.get('page', 1))
    # 한 페이지 당 5개 피드
    feed_count = 5
    paginator  = Paginator(feeds, feed_count)
    
    last_page = paginator.num_pages

    # 최대페이지보다 클 경우 요청 페이지를 마지막 페이지로
    current_page = min(current_page, last_page)

    # 출력 범위 설정
    print_range = 5
    start_page = (current_page - 1) // print_range * print_range + 1
    end_page = min(start_page + (print_range - 1), last_page)
    
    board = paginator.page(current_page)
    context = {'board':board,  'board_number' : current_page, 'page_range' : range(start_page, end_page + 1),}

    return render(request, 'bulletin/board.html', context)

def feed(request, feed_id):
    # feed = Post.objects.get(id = feed_id)
    feed = get_object_or_404(BulletinFeed, id = feed_id)
    reply_list = BulletinReply.objects.filter(bulletinfeed=feed_id)
    return render(request, 'bulletin/feed.html', {'feed':feed, 'reply_list':reply_list})

def upload(request):
    if request.method == "POST":
        form = BulletinFeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.upload_time = timezone.now()
            feed.user = request.user
            feed.save()
            return redirect("../")
    elif not request.user.is_authenticated:
        # 팝업창 어떻게 띄우지..
        return redirect('/log_sign/login')
    else:
        form = BulletinFeedForm()

    return render(request, 'bulletin/upload.html', {'form':form})
def add_reply(request):
    reply   = BulletinReply()
    feed_id = request.data.get('feed_id')
    user_id = request.data.get('user_id')
    content = request.data.get('content')

    reply.bulletinfeed = BulletinFeed.objects.get(id = feed_id)
    reply.user         = User.objects.get(id = user_id)
    reply.content      = content
    reply.created_at   = timezone.now()
    reply.save()
    dest = '/bulletin/' + str(feed_id)
    return redirect(dest)
    
def modify(request, post_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    if request.method == 'GET':
        form = BulletinForm()
        context['forms'] = form
        return render(request, 'bulletin/upload.html', context)

    elif request.method == "POST":
        form = BulletinForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.write_date = timezone.now()
            feed.save()
            return redirect("../")
        else:
            context['forms'] = form
            if form.errors:
                for value in form.errors.values():
                    context['error'] = value
            return render(request, 'bulletin/upload.html', context)
    


def modify(request, feed_id):
    login_session = request.session.get('login_session', '')
    context = {'login_session' : login_session}

    # post = get_object_or_404(Post, id=post_id)
    feed = BulletinFeed.objects.get(id=feed_id)
    

    # if post.author.id != login_session:
    #     return redirect('../bulletin/post_detail/{post_id}/')

    if request.method == "POST":
        form = BulletinForm(request.POST, instance=feed)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.modify_date = timezone.now()

            feed.save()
            return redirect('/bulletin/' + str(feed.id), context)
    else:
        form = BulletinForm(instance=feed)
    
    context = {'form': form}
    return render(request, 'bulletin/post_modify.html', context)


def delete(request, feed_id):
    login_session = request.session.get('login_session', '')
    feed = get_object_or_404(BulletinFeed, id=feed_id)
    
    context = {'feed': feed}

    feed = BulletinFeed.objects.get(id=feed_id)
    feed.delete()
    return redirect('/bulletin')