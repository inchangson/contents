from .models import BulletinFeed
from django import forms

class BulletinFeedForm(forms.ModelForm):
    class Meta:
        model = BulletinFeed
        fields = ['title', 'content']
        
        labels = {'title': '제목','content': '내용',}