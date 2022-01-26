from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import BulletinFeed
from .forms import BulletinForm
from django.db.models import Q
from django.utils import timezone

# Create your views here.

def board(request):
    # 게시판 (등록일 기준 최신 순- id desc)
    feeds = BulletinFeed.objects.all().order_by('-write_date')
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
    return render(request, 'bulletin/feed.html', {'feed':feed})

def upload(request):
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