from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile, MealOption


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={'autofocus': True, 'autocomplete': 'email'}),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': 'Enter a correct email address and password.',
        'inactive': 'This account is inactive.',
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            self.confirm_login_allowed(self.user_cache)
        return cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(self.error_messages['inactive'], code='inactive')

    def get_user(self):
        return self.user_cache


class ExtendedRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'role', 'allergen_free_text']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if UserProfile.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email address already exists.'
            )
        return email

class MealOptionForm(forms.ModelForm):
    class Meta:
        model = MealOption
        fields = ['name', 'description', 'vendor', 'price', 'contains_allergens', 'is_active']

    def clean_price(self):
        """Custom backend validation checking for invalid financial entries."""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price parameters must express a positive numeric amount.")
        return price
