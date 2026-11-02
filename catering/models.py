from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserProfile(AbstractUser):
    """
    Extends built-in auth user to isolate roles, phone details, and allergens.
    """
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Office Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        default='',
        help_text="Enter contact phone number"
    )
    allergen_free_text = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Provide comma-separated values (e.g., peanuts, dairy, gluten)"
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


class MealOption(models.Model):
    """
    Stores individual daily food selections controlled by Admin CRUD pathways.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    vendor = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    contains_allergens = models.CharField(max_length=200, blank=True, help_text="Comma-separated listing")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Implements backend entity mapping to bridge User Profiles securely to Meal Choices.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders')
    meal_option = models.ForeignKey(MealOption, on_delete=models.PROTECT, related_name='ordered_meals')
    order_date = models.DateField(default=timezone.now)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.meal_option.name} for {self.order_date}"
