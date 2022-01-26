from django.shortcuts import redirect, render
from .models import User
from rest_framework.views import APIView

from bulletin.models import Post
from django.core.paginator import Paginator
# Create your views here.


class Main(APIView):
    def get(self, request):
        feeds = Post.objects.all().order_by('-write_date')
        page  = Paginator(feeds, 5).page(1)
        return render(request, 'log_sign/main.html', {'bulletin_page':page})


def signup(request):
    if request.method == 'POST':
        # Check dupl. of User ID/Email
        if User.objects.filter(username=request.POST['username']).exists() or User.objects.filter(email=request.POST["email"]).exists():
            return render(request, 'log_sign/signup_error_id_email.html')

        username = request.POST["username"]
        raw_password = request.POST["password1"]
        password = request.POST["password2"]

        # Check Password Typo
        if raw_password != password:
            return render(request, 'log_sign/signup_error_pw.html')
        petname = request.POST["petname"]
        email = request.POST["email"]

        user = User.objects.create_user(username, email, raw_password)
        user.petname = petname
        user.save()
        return redirect("log_sign:login")
    return render(request, 'log_sign/signup.html')


def map(request):
    return render(request, 'map.html')
