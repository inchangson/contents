from django.urls import path
from . import views
from .views import UploadFeed, CreateReply, LikeFeed
from django.conf import settings
from django.conf.urls.static import static

app_name = 'photo_zone'
urlpatterns = [
    path('main_content/', views.main_content, name='main_content'),
    path('upload', UploadFeed.as_view()),
    path('reply/create', CreateReply.as_view(), name='reply_create'),

    path('like/', LikeFeed.as_view(), name='like'),

    path('deleteFeed/<int:feed_id>', views.deleteFeed, name='deleteFeed'),

]
