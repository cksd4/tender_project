from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from .models import UserProfile, MealOption

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

    def save(self, commit=True):
        user = super().save(commit=False)
        email_prefix = self.cleaned_data['email'].partition('@')[0]
        base_username = slugify(email_prefix) or 'user'
        username = base_username[:150]
        suffix = 1
        while UserProfile.objects.filter(username=username).exists():
            suffix_text = f'-{suffix}'
            username = f'{base_username[:150 - len(suffix_text)]}{suffix_text}'
            suffix += 1
        user.username = username

        if commit:
            user.save()
            self.save_m2m()
        return user


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
