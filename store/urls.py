from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="index"),
    path('main/',views.adminpage,name="Admin Page"),
    path('nav/',views.nav,name="Admin Page"),
    path('footer/',views.footer,name="Admin Page"),
]