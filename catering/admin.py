from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, MealOption, Order
from .forms import EmailAuthenticationForm, ExtendedRegistrationForm

admin.site.login_form = EmailAuthenticationForm
admin.site.login_template = 'catering/admin_login.html'


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
	add_form = ExtendedRegistrationForm
	ordering = ('email',)
	list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
	search_fields = ('email', 'first_name', 'last_name')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {
			'fields': (
				'first_name', 'last_name', 'role', 'phone_number',
				'allergen_free_text',
			),
		}),
		('Permissions', {
			'fields': (
				'is_active', 'is_staff', 'is_superuser', 'groups',
				'user_permissions',
			),
		}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': (
				'email', 'first_name', 'last_name', 'role', 'phone_number',
				'allergen_free_text', 'password1', 'password2',
			),
		}),
	)

admin.site.register(MealOption)
admin.site.register(Order)
