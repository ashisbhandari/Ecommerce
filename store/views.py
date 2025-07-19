from django.shortcuts import render,redirect,HttpResponse
# Create your views here.

def home(request):
    return render(request, 'store/index.html')
def adminpage(request):
    return render(request,"store/admin-page.html")
