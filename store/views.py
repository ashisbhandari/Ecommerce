from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser

from django.contrib.auth.hashers import make_password, check_password


# def home(request):
#     if request.method == 'POST':
#         form_type = request.POST.get('form_type')

#         if form_type == 'login':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             try:
#                 user = CustomUser.objects.get(username=username)
#                 if user.password == password:
#                     auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                     messages.success(request, f"Welcome back, {user.username}!")
#                     return redirect('/main/')
#                 else:
#                     messages.error(request, "Invalid password.")
#                     return redirect('/footer/')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, "User does not exist.")
#             return redirect('/nav/')
#     return render(request, 'store/index.html')

def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = CustomUser.objects.get(username=username)
                if user.password == password:
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, f"Welcome back, {user.username}!")
                    return redirect('/main/')
                else:
                    messages.error(request, "Invalid password.")
                    return redirect('/footer/')
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
            return redirect('/nav/')

        elif form_type == 'signup':
            username = request.POST.get('username')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            address = request.POST.get('address')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('index')

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('index')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('index')

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                contact=contact,
                address=address,
            )
            user.save()
            messages.success(request, "User registered successfully. Please login.")
            return redirect('index')

    return render(request, 'store/index.html')
# def home(request):
#     if request.method == 'POST':
#         form_type = request.POST.get('form_type')

#         if form_type == 'login':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request, username=username, password=password)
#             if user:
#                 auth_login(request, user)
#                 messages.success(request, f"Welcome back, {user.username}!")
#                 return redirect('/main/')  # redirect where you want after login
#             else:
#                 messages.error(request, "Invalid username or password.")
#                 return redirect('/nav/')

#         elif form_type == 'signup':
#             username = request.POST.get('username')
#             email = request.POST.get('email')
#             contact = request.POST.get('contact')
#             address = request.POST.get('address')
#             password = request.POST.get('password')
#             confirm_password = request.POST.get('confirm_password')

#             if password != confirm_password:
#                 messages.error(request, "Passwords do not match.")
#                 return redirect('index')

#             if CustomUser.objects.filter(username=username).exists():
#                 messages.error(request, "Username already exists.")
#                 return redirect('index')

#             if CustomUser.objects.filter(email=email).exists():
#                 messages.error(request, "Email already registered.")
#                 return redirect('index')

#             user = CustomUser.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
#                 contact=contact,
#                 address=address,
#             )
#             user.save()
#             messages.success(request, "User registered successfully. Please login.")
#             return redirect('index')

#     return render(request, 'store/index.html')

def adminpage(request):
    return render(request,"store/admin-page.html")
def nav(request):
    return render(request,"store/navbar.html")
def footer(request):
    return render(request,"store/footer.html")
