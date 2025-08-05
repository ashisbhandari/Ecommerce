from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser,Product
from decimal import Decimal, InvalidOperation
from django.contrib import messages
import json
from bson.decimal128 import Decimal128




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
        status = request.POST.get('product_status') 
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

            return redirect('/clicktoshop')
        
        # update stock level of product
        elif form_type == 'update_stock':
            product_id_or_name = request.POST.get('product_id', '').strip()
            quantity_input = request.POST.get('product_stock', '').strip()
            price_input = request.POST.get('price', '').strip()
            try:
                quantity_change = int(quantity_input)
            except ValueError:
                messages.error(request, "Please enter a valid integer for stock quantity.")
                return redirect('/clicktoshop')

            try:
                if product_id_or_name.isdigit():
                    product = Product.objects.get(id=int(product_id_or_name))
                else:
                    product = Product.objects.get(name__iexact=product_id_or_name)

                new_quantity = product.quantity + quantity_change
                if new_quantity < 0:
                    messages.error(request, f"Insufficient stock. Current stock: {product.quantity}")
                    return redirect('/clicktoshop')

                product.quantity = new_quantity
                if new_quantity <= 0:
                    product.product_status = "Out of Stock"
                else:
                    product.product_status = "Available"

                if price_input:
                    try:
                        product.price = Decimal(price_input)
                    except InvalidOperation:
                        messages.error(request, "Invalid price format.")
                        return redirect('/clicktoshop')

                product.save()
                change_type = "increased" if quantity_change >= 0 else "decreased"
                messages.success(request, f"Stock {change_type} for '{product.name}'. New quantity: {new_quantity}")

            except Product.DoesNotExist:
                messages.error(request, "Product not found. Please check the ID or Name.")

        return redirect('/clicktoshop')
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

# def product(request, id):
#     product = get_object_or_404(Product, id=id)
#     products = Product.objects.exclude(id=id)
#     if request.method == "POST":
#         form_type = request.POST.get('form_type')

#         # Add Product
#         if form_type == 'Purchase':
#             name = request.POST.get('product_name').strip()
#             price = request.POST.get('product_price')
#             description = request.POST.get('product_description').strip()
#             category = request.POST.get('product_category')
#             stock = request.POST.get('product_stock')
#             status = request.POST.get('product_status')

#             if Product.objects.filter(name__iexact=name).exists():
#                 messages.error(request, f"Product '{name}' already exists.")
#             else:
#                 product = Product(
#                     name=name,
#                     price=price,
#                     description=description,
#                     category=category,
#                     quantity=stock,
#                     product_status=status,
#                     image=image
#                 )
#                 product.save()
#                 messages.success(request, f"Product '{name}' added successfully.")

#             return redirect('/clicktoshop')

#     return render(request, 'store/product.html', {'product': product,'products':products})
from .forms import buyproduct
def product(request, id):
    product = get_object_or_404(Product, id=id)
    products = Product.objects.exclude(id=id)

    if request.method == "POST" and request.POST.get("form_type") == "Purchase":
        form = buyproduct(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your order has been confirmed.")
            return redirect('/')
        else:
            messages.error(request, "There was an error in the form. Please try again.")
    else:
        form = buyproduct()

    return render(request, 'store/product.html', {
        'product': product,
        'products': products,
        'form': form
    })

def contact(request):
    return render(request,"store/contact_us.html")
def test(request):
    return render(request,"store/test.html")