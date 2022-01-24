from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import BulletinFeed
from .forms import BulletinFeedForm
from django.utils import timezone

# Create your views here.
def board(request):
    feeds = BulletinFeed.objects.all().order_by('-id')
    current_page      = int(request.GET.get('page', 1))
    paginator = Paginator(feeds, 5)
    
    last_page = paginator.num_pages
    current_page = min(current_page, last_page)
    start_page = (current_page - 1) // 10 * 10 + 1
    end_page = min(start_page + 9, last_page)

    board = paginator.page(current_page)
    return render(request, 'bulletin/board.html',{'board':board, 'page_range' : range(start_page, end_page + 1)})


def feed(request, feed_id):
    # feed = BulletinFeed.objects.get(id = feed_id)
    feed = get_object_or_404(BulletinFeed, id = feed_id)
    return render(request, 'bulletin/feed.html', {'feed':feed})

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def upload(request):
    if request.method == "POST":
        form = BulletinFeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.upload_time = timezone.now()
            feed.save()
            return redirect("../")
    else:
        form = BulletinFeedForm()
    return render(request, 'bulletin/upload.html', {'form':form})