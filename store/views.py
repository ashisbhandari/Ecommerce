from django.shortcuts import render,redirect
# Create your views here.

def home(request):
    return render(request, 'store/index.html')
def adminpage(request):
    return render(request,"store/admin-page.html")
