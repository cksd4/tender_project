from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.user_register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catering/employee_login.html', authentication_form=EmailAuthenticationForm), name='login'),
    path('employee-login/', auth_views.LoginView.as_view(template_name='catering/employee_login.html', authentication_form=EmailAuthenticationForm), name='employee_login'),
    path('vendor-login/', auth_views.LoginView.as_view(template_name='catering/vendor_login.html', authentication_form=EmailAuthenticationForm), name='vendor_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='employee_login'), name='logout'),
    path('order/place/<int:meal_id>/', views.place_order, name='place_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin-management/', views.admin_panel, name='admin_panel'),
    path('admin-management/edit/<int:meal_id>/', views.edit_meal, name='edit_meal'),
    path('admin-management/delete/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('account-settings/delete/', views.delete_account, name='delete_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='catering/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='catering/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='catering/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='catering/password_reset_complete.html'), name='password_reset_complete'),
]
