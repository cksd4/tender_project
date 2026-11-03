from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.views.decorators.http import require_POST
from .models import MealOption, Order
from .forms import ExtendedRegistrationForm, MealOptionForm


def has_admin_access(user):
    return user.is_superuser or user.role == 'admin'


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not has_admin_access(request.user):
            messages.error(request, "Access Terminated: Insufficient administrative privileges.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)

    return wrapped_view


def user_register(request):
    if request.method == 'POST':
        form = ExtendedRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account registration verified successfully!")
            return redirect('dashboard')
    else:
        form = ExtendedRegistrationForm()
    return render(request, 'catering/register.html', {'form': form})


@login_required
def dashboard(request):
    if has_admin_access(request.user):
        return redirect('admin_panel')

    meals = MealOption.objects.filter(is_active=True)
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catering/dashboard.html', {'meals': meals, 'user_orders': user_orders})

@login_required
def place_order(request, meal_id):
    meal = get_object_or_404(MealOption, id=meal_id)

    user_allergens = [
        item.strip().lower()
        for item in request.user.allergen_free_text.split(',')
        if item
    ]
    meal_allergens = [
        item.strip().lower()
        for item in meal.contains_allergens.split(',')
        if item
    ]
    has_allergy_risk = any(
        allergen in meal_allergens for allergen in user_allergens
    )

    Order.objects.create(
        user=request.user,
        meal_option=meal,
        meal_name=meal.name,
    )

    if has_allergy_risk:
        messages.warning(
            request,
            "Order confirmed, but warning: This choice carries ingredients "
            "flagged on your account.",
        )
    else:
        messages.success(request, "Your office lunch booking has been securely captured.")

    return redirect('dashboard')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.info(request, "Your reservation request was removed cleanly.")
    return redirect('dashboard')


@login_required
@admin_required
def admin_panel(request):
    all_meals = MealOption.objects.annotate(order_count=Count('ordered_meals'))
    all_orders = Order.objects.all()
    
    if request.method == 'POST':
        form = MealOptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New menu component appended seamlessly.")
            return redirect('admin_panel')
    else:
        form = MealOptionForm()

    context = {
        'all_meals': all_meals,
        'all_orders': all_orders,
        'form': form,
    }
    return render(request, 'catering/admin_panel.html', context)

@login_required
@admin_required
def edit_meal(request, meal_id):
    meal = get_object_or_404(MealOption, id=meal_id)
    
    if request.method == 'POST':
        form = MealOptionForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{meal.name}' was modified successfully.")
            return redirect('admin_panel')
    else:
        form = MealOptionForm(instance=meal)
        
    return render(request, 'catering/edit_meal.html', {'form': form, 'meal': meal})

@login_required
@require_POST
@admin_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(MealOption, id=meal_id)
    meal_name = meal.name
    meal.delete()
    messages.info(request, f"Menu option '{meal_name}' has been deleted.")
    return redirect('admin_panel')

@login_required
def account_settings(request):
    if request.method == 'POST':
        user = request.user
        email_input = request.POST.get('email', '').strip()
        phone_input = request.POST.get('phone_number', '').strip()
        allergen_input = request.POST.get('allergen_free_text', '').strip()

        if not email_input or not phone_input:
            messages.error(request, "Update Rejected: Email and Phone Number parameters are mandatory.")
        else:
            user.email = email_input
            user.phone_number = phone_input
            user.allergen_free_text = allergen_input
            user.save()
            messages.success(request, "Your account configurations have updated smoothly.")
            return redirect('account_settings')

    return render(request, 'catering/account_settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.info(request, "Your enterprise account profile has been completely deleted.")
        return redirect('employee_login')

    return redirect('account_settings')
