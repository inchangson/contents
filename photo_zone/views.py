from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed, Reply
from log_sign.models import User
from rest_framework.response import Response
import os
from config.settings import MEDIA_ROOT
from uuid import uuid4


def main_content(request):
    print(request.user.username, request.user.email)
    # email = request.session.get('username', None)
    email = request.user.username
    print(email)
    # email = 'a@a.com'
    if email is None:
        return render(request, 'log_sign/login.html')

    user = User.objects.filter(username=email).first()
    print(user)
    if user is None:
        return render(request, 'log_sign/login.html')

    feed_object_list = Feed.objects.all().order_by('-id')
    feed_list = []
    for feed in feed_object_list:
        reply_list = Reply.objects.filter(feed_id=feed.id)
        feed_list.append(dict(
            id=feed.id,
            username=feed.username,
            image=feed.image,
            content=feed.content,
            reply_list=reply_list,
        ))
    return render(request,
                  'photo_zone/main.html',
                  context=dict(feeds=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']  # 파일 읽기 권장 request.FILES.get('file')
        uuid_name = uuid4().hex  # 랜덤값 부여(파일 이름이 불규칙 적이기 때문에)
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')  # 파일을 제외한 데이터(content)
        image = uuid_name
        username = request.data.get('username')  # 파일을 제외한 데이터(id)

        Feed.objects.create(content=content, image=image,
                            username=username, like_count=0)  # create로 생성

        return Response(status=200)


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
