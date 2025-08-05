from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="index"),
    path('main/',views.adminpage,name="Admin Page"),
    path('nav/',views.nav,name="Admin Page"),
    path('footer/',views.footer,name="footer"),
    # path('ashish/',views.update_stock,name="Admin Page"),
    path('clicktoshop/',views.ashish,name="Admin Page"),
    path('product/<int:id>/',views.product,name="product"),
    path('contact/',views.contact,name="contact us"),
    path('test/',views.test,name="contact us"),
]