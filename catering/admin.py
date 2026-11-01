from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MealOption, Order

# Register your custom AbstractUser model safely with authentication workflows
admin.site.register(UserProfile, UserAdmin)

# Register your custom CRUD operational models
admin.site.register(MealOption)
admin.site.register(Order)
