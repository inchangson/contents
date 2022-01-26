from django.db import models
from psutil import users
from sqlalchemy import null
from log_sign.models import User
# Create your models here.

# 게시판 피드 객체
class BulletinFeed(models.Model):
#    id = models.IntegerField(primary_key=True)
    title       = models.CharField(max_length=255,  null=True)
    write_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True) 
    #txt_path로 바꿀지 확인
    content     = models.TextField(max_length=255,  null=True)    
    img_path    = models.CharField(max_length=255,  null=True)
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    view_count  = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    def update_counter(self):
        self.view_count = self.view_count + 1
        self.save()