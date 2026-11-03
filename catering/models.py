from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('An email address is required.')
        email = self.normalize_email(email).strip().lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if not extra_fields['is_staff']:
            raise ValueError('A superuser must have is_staff=True.')
        if not extra_fields['is_superuser']:
            raise ValueError('A superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    """
    Extends built-in auth user to isolate roles, phone details, and allergens.
    """
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Office Admin'),
    ]
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserProfileManager()

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
        return f"{self.email} - {self.get_role_display()}"

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
    meal_name = models.CharField(max_length=100, blank=True, default='')
    meal_option = models.ForeignKey(
        MealOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordered_meals',
    )
    order_date = models.DateField(default=timezone.now)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.meal_option_id and not self.meal_name:
            self.meal_name = self.meal_option.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} reserved {self.meal_name} for {self.order_date}"
