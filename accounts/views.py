from django.shortcuts import render

from vendor.forms import VendorForm
from .forms import UserForm
from django.shortcuts import redirect
from .models import User, UserProfile
from django.contrib import messages, auth
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # # Now user has the form data
            # user = form.save(commit=False)
            # user.set_password(password)
            # # assigning role to the user
            # user.role = User.CUSTOMER
            # user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            print(f'-----------------{user}------------------------')
            print(f'-----------------{user.role}------------------------')
            
            user.role = User.CUSTOMER
            print("This is my user role: ", user.role)
            user.save()
            messages.success(request, "Your account has successfully register")
            print("User is created")
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        "form": form
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        # store the data and create user
        form = UserForm(request.POST)
        # As we are receiving the file thats why we are using request.FILES
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            print(f'-----------------{user}------------------------')
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            userprofile = UserProfile.objects.get(user=user)
            vendor.userprofile = userprofile
            vendor.save()
            messages.success(request, "Your account has been register successfully")
            return redirect('registerVendor')
        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = UserForm() 
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"YOu are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid Login Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged Out")
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')