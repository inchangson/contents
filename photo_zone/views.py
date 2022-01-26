from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Feed, Reply, Like
from log_sign.models import User
from rest_framework.response import Response
import os
from config.settings import MEDIA_ROOT
from uuid import uuid4


# photo_zone 메인 화면
def main_content(request):
    #print(request.user.username, request.user.email)
    username = request.user.username  # 내장로그인 일때 로그인 값 저장
    if username is None:
        return render(request, 'log_sign/login.html')  # username이 없다면 다시 로그인으로

    user = User.objects.filter(username=username).first()
    if user is None:
        return render(request, 'log_sign/login.html')  # username이 없다면 다시 로그인으로

    feed_object_list = Feed.objects.all().order_by('-id')
    feed_list = []
    
    for feed in feed_object_list:
        reply_list = Reply.objects.filter(feed_id=feed.id)
        is_like = Like.objects.filter(feed_id=feed.id, username=username).exists()
        like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()

        feed_list.append(dict(
            id=feed.id,
            username=feed.username,
            image=feed.image,
            content=feed.content,
            reply_list=reply_list,
            like_count=like_count,
            is_like=is_like
        ))                 # feed데이터 저장
    return render(request,
                  'photo_zone/main.html',
                  context=dict(feeds=feed_list, user=user))

# 게시물 업로드


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']  # 파일 읽기 권장 request.FILES.get('file')
        uuid_name = uuid4().hex  # 랜덤값 부여(파일 이름이 불규칙 적이기 때문에)
        # uuid를 사용해 파일마다 유일한 번호 부여
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')  # 파일을 제외한 데이터(content)
        image = uuid_name
        username = request.data.get('username')  # 파일을 제외한 데이터(id)

        Feed.objects.create(content=content, image=image,
                            username=username)  # create로 생성

        return Response(status=200)

# 댓글


class CreateReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id')
        username = request.data.get('username')
        content = request.data.get('content')
        Reply.objects.create(feed_id=feed_id,
                             username=username,
                             content=content
                             )

        return Response(status=200, data=dict(message='댓글 작성 완료.'))


#좋아요
class LikeFeed(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        username = request.data.get('username', None)
        is_like = request.data.get('is_like', True)

        if is_like == 'True' or is_like == 'true':
            is_like =True
        else:
            is_like =False

        Like.objects.create(feed_id=feed_id,
                             username=username,
                             is_like=is_like
                             )

        return Response(status=200, data=dict(message='좋아요를 눌렀습니다.'))

# 게시글 삭제


def deleteFeed(request, feed_id):
    post = Feed.objects.get(id=feed_id)
    post.delete()
    return redirect('/photo_zone/main_content')

