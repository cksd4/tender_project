from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.user_register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catering/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('order/place/<int:meal_id>/', views.place_order, name='place_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin-management/', views.admin_panel, name='admin_panel'),
        path('admin-management/edit/<int:meal_id>/', views.edit_meal, name='edit_meal'),
    path('admin-management/delete/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('account-settings/delete/', views.delete_account, name='delete_account'),

]
