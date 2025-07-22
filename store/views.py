from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser,Product

from django.contrib.auth.hashers import make_password, check_password


def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('/main/')  # redirect where you want after login
            else:
                messages.error(request, "Invalid username or password.")
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
    products = Product.objects.all()
    return render(request, 'store/index.html',{'products': products})

def adminpage(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        image = request.FILES.get('product_image')  # Use request.FILES for file uploads
        description = request.POST.get('product_description')
        category = request.POST.get('product_category')
        stock = request.POST.get('product_stock')
        status = request.POST.get('product_status')  # Typo fixed: 'producy_status' → 'product_status'

        # Save to the database
        Product.objects.create(
            name=name,
            price=price,
            image=image,
            description=description,
            category=category,
            quantity=stock,
            product_status=status
        )

        return redirect('/main')  

    return render(request, "store/admin-page.html")

# def product_list(request):
#     products = Product.objects.all()  # Get all products from DB
#     return render(request, 'store/index.html', {'products': products})

def nav(request):
    return render(request,"store/navbar.html")
def footer(request):
    return render(request,"store/footer.html")
# def ashish(request):
#     if request.method == 'POST':
#         name = request.POST.get('product_name')
#         price = request.POST.get('product_price')
#         image = request.FILES.get('product_image')  # Use request.FILES for file uploads
#         description = request.POST.get('product_description')
#         category = request.POST.get('product_category')
#         stock = request.POST.get('product_stock')
#         status = request.POST.get('product_status')  # Typo fixed: 'producy_status' → 'product_status'

#         # Save to the database
#         Product.objects.create(
#             name=name,
#             price=price,
#             image=image,
#             description=description,
#             category=category,
#             quantity=stock,
#             product_status=status
#         )

#         return redirect('/main')
#     products = Product.objects.all()
#     return render(request, 'store/ok.html',{'products': products})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt  # only if needed for API; try to avoid disabling CSRF
from django.contrib import messages

from .models import Product  # adjust import per your app structure



from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib import messages
from .models import Product
from django.core.serializers import serialize
import json
from bson.decimal128 import Decimal128

def ashish(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        # Add Product
        if form_type == 'add_product':
            name = request.POST.get('product_name').strip()
            price = request.POST.get('product_price')
            description = request.POST.get('product_description').strip()
            category = request.POST.get('product_category')
            stock = request.POST.get('product_stock')
            status = request.POST.get('product_status')
            image = request.FILES.get('product_image')

            if Product.objects.filter(name__iexact=name).exists():
                messages.error(request, f"Product '{name}' already exists.")
            else:
                product = Product(
                    name=name,
                    price=price,
                    description=description,
                    category=category,
                    quantity=stock,
                    product_status=status,
                    image=image
                )
                product.save()
                messages.success(request, f"Product '{name}' added successfully.")

            return redirect('/ashish')

        elif form_type == 'update_stock':
            product_id_or_name = request.POST.get('product_id').strip()
            stock = request.POST.get('product_stock')
            status = request.POST.get('product_status')

            try:
                if product_id_or_name.isdigit():
                    product = Product.objects.get(id=int(product_id_or_name))
                else:
                    product = Product.objects.get(name__iexact=product_id_or_name)

                product.quantity = stock
                product.product_status = status
                product.save()
                messages.success(request, f"Stock updated for '{product.name}'.")
            except Product.DoesNotExist:
                messages.error(request, "Product not found.")

            return redirect('/ashish')

    products = Product.objects.all().order_by('id')
    product_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price.to_decimal()) if isinstance(p.price, Decimal128) else float(p.price),
            "stock": p.quantity,
            "status": p.product_status,
            "description": p.description,
            "category": p.category,
        } for p in products
    ]
    return render(request, 'store/ok.html', {
        'products': products,
        'product_json': json.dumps(product_data)
    })
