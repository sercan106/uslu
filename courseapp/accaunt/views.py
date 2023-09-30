from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout #bulogin işlemleri için gereken kütüphane
# Create your views here.

def user_login(request):
    if request.user.is_authenticated and 'next' in request.GET:#eğer superuser kullanıcı değilse
        return render(request, 'accaunt/login.html' ,{'error':'Yetkili kullanıcı değilsiniz'})
        
       
        
    if request.method=='POST':
        print("post işlemi oldu")
        username=request.POST["username"]
        password=request.POST["password"]
        print(username,password)
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('ev')
        else:
            return render(request, 'accaunt/login.html' ,{'error':'veriler eşleşmedi'})
    else:
        return render(request, 'accaunt/login.html')

def user_register(request):
    return render(request, 'accaunt/register.html')


def user_logout(request):
    logout(request)
    return redirect('ev')