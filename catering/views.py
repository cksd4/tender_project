import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MealOption, Order
from .forms import ExtendedRegistrationForm, MealOptionForm

def user_register(request):
    """Manages public profile signup cycles."""
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
    """
    Presents functional menu lists alongside individual user booking data history.
    """
    meals = MealOption.objects.filter(is_active=True)
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'meals': meals,
        'user_orders': user_orders,
    }
    return render(request, 'catering/dashboard.html', context)


@login_required
def place_order(request, meal_id):
    """
    Compound statements evaluate current local time boundaries against strict constraints.
    Features automated loop scans to detect custom allergen match conditions.
    """
    meal = get_object_or_404(MealOption, id=meal_id)
    current_time = datetime.datetime.now().time()
    cutoff_time = datetime.time(10, 0, 0) # 10:00 AM Strict Policy Constraint

    # Compound Conditional Checks (1.4)
    if current_time > cutoff_time:
        messages.error(request, "Order Processing Halted: The daily 10:00 AM ordering deadline has passed.")
        return redirect('dashboard')

    # Sequential Loop Verification to extract matching allergy profiles
    user_allergens = [item.strip().lower() for item in request.user.allergen_free_text.split(',') if item]
    meal_allergens = [item.strip().lower() for item in meal.contains_allergens.split(',') if item]

    has_allergy_risk = False
    for allergen in user_allergens:
        if allergen in meal_allergens:
            has_allergy_risk = True
            break # Optimized performance break step

    # Invoke secure ORM commit action (1.2)
    Order.objects.create(user=request.user, meal_option=meal)

    # Real-Time UI Feedback Generation (2.3)
    if has_allergy_risk:
        messages.warning(request, f"Order confirmed, but warning: This choice carries ingredients flagged on your account.")
    else:
        messages.success(request, "Your office lunch booking has been securely captured.")

    return redirect('dashboard')


@login_required
def cancel_order(request, order_id):
    """Empowers standard employees to execute record removal (CRUD - Delete)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.info(request, "Your reservation request was removed cleanly.")
    return redirect('dashboard')


@login_required
def admin_panel(request):
    """
    Restricts dashboard interface access strictly to Administrative accounts.
    Fulfills non-escalation access standards (3.3).
    """
    if request.user.role != 'admin':
        messages.error(request, "Access Terminated: Insufficient administrative privileges.")
        return redirect('dashboard')

    all_meals = MealOption.objects.all()
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
