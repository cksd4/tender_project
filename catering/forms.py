from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, MealOption

class ExtendedRegistrationForm(UserCreationForm):
    """
    Captures profile configurations safely during registration phases.
    """
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ('role', 'allergen_free_text')


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
