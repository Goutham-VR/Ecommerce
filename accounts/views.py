from django.shortcuts import render
from accounts.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip().lower()
        phone = request.POST.get('phone').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not name:
            return render(request,'accounts/register.html',{'msg': 'Name is required'})
        
        if phone and User.objects.filter(phone=phone).exists():
            return render(request,'accounts/register.html',{'msg': 'Phone number already exists'})
        
        if phone and len(phone) != 10:
            return render(request,'accounts/register.html',{'msg': 'Enter a valid phone number'})
        
        if len(password) < 6:
            return render(request,'accounts/register.html',{'msg': 'Password must be at least 6 characters'})
        
        if password != confirm_password:
            return render(request,'accounts/register.html',{'msg': 'Passwords do not match'})
        
        if User.objects.filter(email=email).exists():
            return render(request,'accounts/register.html',{'msg': 'Email already exists'})
        
        User.objects.create_user(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        return render(request,'accounts/register.html',{'msg': 'Registration Successful'})
    else:
        return render(request,'accounts/register.html')
    
def userlogin(request):
    if request.method == "POST":

        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request, user)
            return render(request,'accounts/login.html',{'msg': 'Login Successful'})
        else:
            return render(request,'accounts/login.html',{'msg': 'Invalid Email or Password'})
    else:
        return render(request,'accounts/login.html')
    
def userlogout(request):

    logout(request)

    return render(
        request,
        'accounts/login.html',
        {'msg': 'Logged Out Successfully'}
    )