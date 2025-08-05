# store/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Product,purchase

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'contact', 'address', 'password1', 'password2')

    # password1 and password2 are built-in fields in UserCreationForm (password and confirm password)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email
    
# forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# product add garne forms
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'quantity', 'product_status', 'image']
class buyproduct(forms.ModelForm):
    class Meta:
        model=purchase
        fields =['user_name','user_address','user_email','user_contact','product_name','product_quantity','product_price','product_description','product_category','total_amount']