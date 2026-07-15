from django.shortcuts import render,redirect
from accounts.models import User
from accounts.models import Address
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

from accounts.models import Address

def addaddress(request):

    if not request.user.is_authenticated:
        return redirect('accounts:userlogin')

    if request.method == "POST":

        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            house=request.POST.get('house'),
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            landmark=request.POST.get('landmark')
        )

        return redirect('accounts:addresslist')

    return render(
        request,
        'accounts/addaddress.html'
    )

def addresslist(request):

    addresses = Address.objects.filter(
        user=request.user
    )

    return render(
        request,
        'accounts/addresslist.html',
        {
            'addresses': addresses
        }
    )

def editaddress(request, address_id):

    address = Address.objects.get(
        id=address_id,
        user=request.user
    )

    if request.method == "POST":

        address.full_name = request.POST.get('full_name')
        address.phone = request.POST.get('phone')
        address.house = request.POST.get('house')
        address.city = request.POST.get('city')
        address.district = request.POST.get('district')
        address.state = request.POST.get('state')
        address.pincode = request.POST.get('pincode')
        address.landmark = request.POST.get('landmark')

        address.save()

        return redirect('accounts:addresslist')

    return render(
        request,
        'accounts/editaddress.html',
        {
            'address': address
        }
    )

def deleteaddress(request, address_id):

    Address.objects.get(
        id=address_id,
        user=request.user
    ).delete()

    return redirect('accounts:addresslist')

def setdefaultaddress(request, address_id):

    Address.objects.filter(
        user=request.user
    ).update(
        is_default=False
    )

    address = Address.objects.get(
        id=address_id,
        user=request.user
    )

    address.is_default = True
    address.save()

    return redirect('accounts:addresslist')