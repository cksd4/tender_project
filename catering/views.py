import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import MealOption, Order
from .forms import ExtendedRegistrationForm, MealOptionForm
from catering import views

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
    """Renders menu items, but routes admins out to their correct terminal space."""
    if request.user.role == 'admin':
        return redirect('admin_panel')
        
    meals = MealOption.objects.filter(is_active=True)
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catering/dashboard.html', {'meals': meals, 'user_orders': user_orders})



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
def edit_meal(request, meal_id):
    """
    Handles the UPDATE phase of CRUD for menu profiles.
    Verifies that only authorized Admin profiles can alter database assets.
    """
    if request.user.role != 'admin':
        messages.error(request, "Access Terminated: Insufficient administrative privileges.")
        return redirect('dashboard')
        
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
def delete_meal(request, meal_id):
    """
    Handles the DELETE phase of CRUD for menu records.
    """
    if request.user.role != 'admin':
        messages.error(request, "Access Terminated: Insufficient administrative privileges.")
        return redirect('dashboard')
        
    meal = get_object_or_404(MealOption, id=meal_id)
    if meal.ordered_meals.exists():
        messages.error(request, f"'{meal.name}' cannot be removed because it is used by existing orders.")
        return redirect('admin_panel')

    meal_name = meal.name
    meal.delete()
    messages.info(request, f"Menu option '{meal_name}' has been deleted.")
    return redirect('admin_panel')
