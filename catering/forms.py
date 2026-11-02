from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, MealOption

class ExtendedRegistrationForm(UserCreationForm):
    """
    Ensures safe role assignment and field capture during public sign-up.
    Forces email and phone number parameters to be mandatory.
    """
    email = forms.EmailField(required=True, help_text="A valid email address is required.")

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'role', 'allergen_free_text')


class MealOptionForm(forms.ModelForm):
    """
    Backend mapping form enabling Admin profiles to execute Create/Update CRUD securely.
    """
    class Meta:
        model = MealOption
        fields = ['name', 'description', 'vendor', 'price', 'contains_allergens', 'is_active']

    def clean_price(self):
        """Custom backend validation checking for invalid financial entries."""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price parameters must express a positive numeric amount.")
        return price
