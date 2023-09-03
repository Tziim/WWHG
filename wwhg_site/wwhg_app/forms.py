from django import forms
from .models import UserProfile, CartItem, ContactInfo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'home_address', 'city', 'country', 'postcode', 'card_name',
                  'card_number', 'exp_month', 'exp_year', 'cvv']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.exclude(pk=self.instance.user.id).filter(
            email=email)

        if user.exists():
            raise forms.ValidationError(
                "This email address is already in use.")

        return email


class CartItemUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'email', 'phone_number', 'question', ]
