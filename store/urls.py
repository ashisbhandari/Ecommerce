from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="index"),
    path('main/',views.adminpage,name="Admin Page"),
]