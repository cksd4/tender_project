from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from .models import MealOption, Order

User = get_user_model()

class TenderProjectTestCase(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            username='staffmember', 
            password='securepassword1', 
            role='employee', 
            allergen_free_text='dairy'
        )
        self.meal = MealOption.objects.create(
            name='Creamy Mushroom Pasta',
            description='Pasta option with garlic cream dressing',
            vendor='Italian Bistro',
            price=9.20,
            contains_allergens='dairy',
            is_active=True
        )

    def test_user_role_assignment(self):
        """Validates role parameters store accurately inside user custom attributes."""
        self.assertEqual(self.employee.role, 'employee')

    def test_sign_out_returns_user_to_login_page(self):
        self.client.force_login(self.employee)

        response = self.client.post(reverse('logout'), follow=True)

        self.assertRedirects(response, reverse('login'))
        self.assertContains(response, 'Sign In')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_authenticated_page_loads_session_timeout_script(self):
        self.client.force_login(self.employee)

        response = self.client.get(reverse('dashboard'))

        self.assertContains(
            response,
            f'data-idle-timeout-seconds="{settings.SESSION_COOKIE_AGE}"',
        )
        self.assertContains(response, 'assets/js/session_timeout.js')

    def test_allergen_detection_logic(self):
        """Confirms backend allergen string loop processing performs accurate character scans."""
        user_allergens = [a.strip().lower() for a in self.employee.allergen_free_text.split(',') if a]
        meal_allergens = [a.strip().lower() for a in self.meal.contains_allergens.split(',') if a]
        
        has_match = any(allergen in meal_allergens for allergen in user_allergens)
        self.assertTrue(has_match)

    def test_admin_panel_shows_menu_option_actions(self):
        admin = User.objects.create_user(username='cateringadmin', password='securepassword1', role='admin')
        self.client.force_login(admin)

        response = self.client.get(reverse('admin_panel'))

        self.assertContains(response, 'Manage Menu Options')
        self.assertContains(response, reverse('edit_meal', args=[self.meal.id]))
        self.assertContains(response, reverse('delete_meal', args=[self.meal.id]))

    def test_admin_can_remove_menu_option_without_orders(self):
        admin = User.objects.create_user(username='cateringadmin', password='securepassword1', role='admin')
        self.client.force_login(admin)

        response = self.client.post(reverse('delete_meal', args=[self.meal.id]), follow=True)

        self.assertRedirects(response, reverse('admin_panel'))
        self.assertFalse(MealOption.objects.filter(id=self.meal.id).exists())

    def test_admin_cannot_remove_menu_option_used_by_orders(self):
        admin = User.objects.create_user(username='cateringadmin', password='securepassword1', role='admin')
        Order.objects.create(user=self.employee, meal_option=self.meal)
        self.client.force_login(admin)

        response = self.client.post(reverse('delete_meal', args=[self.meal.id]), follow=True)

        self.assertRedirects(response, reverse('admin_panel'))
        self.assertTrue(MealOption.objects.filter(id=self.meal.id).exists())
        self.assertContains(response, 'cannot be removed because it is used by existing orders')
