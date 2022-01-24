from django.shortcuts import redirect, render
from .models import User
from rest_framework.views import APIView

# Create your views here.
class Main(APIView):
    def get(self, request):
        return render(request, 'log_sign/main.html')

def signup(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password1"]
        petname = request.POST["petname"]
        email = request.POST["email"]

        user = User.objects.create_user(username, email, password)
        user.petname = petname
        user.save()
        return redirect("log_sign:login")
    # return render(request, 'log_sign/signup.html', {'form': form})
    return render(request, 'log_sign/signup.html')