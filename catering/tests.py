from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from .models import MealOption, Order

User = get_user_model()

class TenderProjectTestCase(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            email='staffmember@example.com',
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

    def test_email_is_the_only_user_identifier(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertNotIn(
            'username',
            [field.name for field in User._meta.get_fields()],
        )
        self.assertTrue(User._meta.get_field('email').unique)

    def test_user_role_assignment(self):
        """Validates role parameters store accurately inside user custom attributes."""
        self.assertEqual(self.employee.role, 'employee')

    def test_sign_out_returns_user_to_login_page(self):
        self.client.force_login(self.employee)

        response = self.client.post(reverse('logout'), follow=True)

        self.assertRedirects(response, reverse('employee_login'))
        self.assertContains(response, 'Employee Hub')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_employee_login_page_renders(self):
        response = self.client.get(reverse('employee_login'))
        legacy_response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Employee Hub')
        self.assertEqual(legacy_response.status_code, 200)
        self.assertContains(legacy_response, 'Employee Hub')

    def test_existing_users_can_log_in_with_email(self):
        self.assertTrue(
            self.client.login(
                email='staffmember@example.com', password='securepassword1'
            )
        )

    def test_registration_creates_distinct_email_accounts(self):
        registration_data = {
            'email': 'new.employee@example.com',
            'first_name': 'New',
            'last_name': 'Employee',
            'phone_number': '07700000000',
            'role': 'employee',
            'allergen_free_text': '',
            'password1': 'TenderPassword123!',
            'password2': 'TenderPassword123!',
        }

        first_response = self.client.post(
            reverse('register'), registration_data
        )
        registration_data['email'] = 'new.employee@another.example'
        second_response = self.client.post(
            reverse('register'), registration_data
        )

        first_user = User.objects.get(email='new.employee@example.com')
        second_user = User.objects.get(email='new.employee@another.example')
        self.assertRedirects(first_response, reverse('dashboard'))
        self.assertRedirects(second_response, reverse('dashboard'))
        self.assertNotEqual(first_user.pk, second_user.pk)

    def test_employee_can_register_and_log_in_with_email(self):
        email = 'employee.login@example.com'
        password = 'TenderPassword123!'
        registration_response = self.client.post(reverse('register'), {
            'email': email,
            'first_name': 'Employee',
            'last_name': 'Account',
            'phone_number': '07700000000',
            'role': 'employee',
            'allergen_free_text': '',
            'password1': password,
            'password2': password,
        })

        user = User.objects.get(email=email)
        self.assertEqual(user.role, 'employee')
        self.assertRedirects(registration_response, reverse('dashboard'))
        self.client.post(reverse('logout'))

        login_response = self.client.post(
            reverse('employee_login'),
            {'email': email, 'password': password},
            follow=True,
        )

        self.assertRedirects(login_response, reverse('dashboard'))
        self.assertContains(login_response, 'Daily Catering Submissions Portal')

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(
            email='existing@example.com',
            password='securepassword1',
        )

        response = self.client.post(reverse('register'), {
            'email': 'existing@example.com',
            'first_name': 'Existing',
            'last_name': 'User',
            'phone_number': '07700000000',
            'role': 'employee',
            'allergen_free_text': '',
            'password1': 'TenderPassword123!',
            'password2': 'TenderPassword123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'An account with this email address already exists.'
        )
        self.assertEqual(
            User.objects.filter(email='existing@example.com').count(), 1
        )

    def test_authenticated_page_loads_session_timeout_script(self):
        self.client.force_login(self.employee)

        response = self.client.get(reverse('dashboard'))

        self.assertContains(
            response,
            f'data-idle-timeout-seconds="{settings.SESSION_COOKIE_AGE}"',
        )
        self.assertContains(response, 'assets/js/session_timeout.js')

    def test_account_settings_displays_user_id_instead_of_username(self):
        self.client.force_login(self.employee)

        response = self.client.get(reverse('account_settings'))

        self.assertContains(response, f'value="{self.employee.pk}"')
        self.assertNotContains(response, 'Username (Fixed)')

    def test_admin_orders_display_customer_user_id(self):
        admin = User.objects.create_user(
            email='cateringadmin@example.com',
            password='securepassword1',
            role='admin',
        )
        self.employee.first_name = 'Staff'
        self.employee.save(update_fields=['first_name'])
        Order.objects.create(user=self.employee, meal_option=self.meal)
        self.client.force_login(admin)

        response = self.client.get(reverse('admin_panel'))

        self.assertContains(response, f'Account ID: {self.employee.pk}')
        self.assertContains(response, 'Customer:</strong> Staff')

    def test_allergen_detection_logic(self):
        """Confirms backend allergen string loop processing performs accurate character scans."""
        user_allergens = [a.strip().lower() for a in self.employee.allergen_free_text.split(',') if a]
        meal_allergens = [a.strip().lower() for a in self.meal.contains_allergens.split(',') if a]
        
        has_match = any(allergen in meal_allergens for allergen in user_allergens)
        self.assertTrue(has_match)

    def test_admin_panel_shows_menu_option_actions(self):
        admin = User.objects.create_user(
            email='cateringadmin@example.com',
            password='securepassword1',
            role='admin',
        )
        self.client.force_login(admin)

        response = self.client.get(reverse('admin_panel'))

        self.assertContains(response, 'Manage Menu Options')
        self.assertContains(response, reverse('edit_meal', args=[self.meal.id]))
        self.assertContains(response, reverse('delete_meal', args=[self.meal.id]))

    def test_superuser_can_access_django_and_catering_admin(self):
        superuser = User.objects.create_superuser(
            email='projectroot@example.com',
            password='securepassword1',
        )
        login_client = Client()
        admin_index = reverse('admin:index')
        login_page = login_client.get(
            reverse('admin:login'), {'next': admin_index}
        )
        login_response = login_client.post(reverse('admin:login'), {
            'email': superuser.email,
            'password': 'securepassword1',
            'next': admin_index,
        })

        self.assertContains(login_page, 'Email address')
        self.assertRedirects(login_response, admin_index)

        self.client.force_login(superuser)

        django_admin_response = self.client.get(reverse('admin:index'))
        dashboard_response = self.client.get(reverse('dashboard'))
        catering_admin_response = self.client.get(reverse('admin_panel'))

        self.assertEqual(django_admin_response.status_code, 200)
        self.assertRedirects(dashboard_response, reverse('admin_panel'))
        self.assertEqual(catering_admin_response.status_code, 200)

        self.client.force_login(superuser)
        add_user_response = self.client.get(
            reverse('admin:catering_userprofile_add')
        )
        self.assertContains(add_user_response, 'name="email"')
        self.assertNotContains(add_user_response, 'name="username"')

    def test_admin_login_accepts_csrf_from_heroku_https_proxy(self):
        client = Client(
            enforce_csrf_checks=True,
            HTTP_HOST='tender-project-app-5c9139cbd71b.herokuapp.com',
            HTTP_X_FORWARDED_PROTO='https',
        )
        login_url = reverse('admin:login')
        origin = 'https://tender-project-app-5c9139cbd71b.herokuapp.com'
        login_page = client.get(login_url, {'next': reverse('admin:index')})

        response = client.post(
            login_url,
            {
                'email': 'nobody@example.com',
                'password': 'invalid-password',
                'next': reverse('admin:index'),
                'csrfmiddlewaretoken': client.cookies['csrftoken'].value,
            },
            HTTP_ORIGIN=origin,
        )

        self.assertEqual(login_page.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a correct email address and password.')

    def test_admin_can_remove_menu_option_without_orders(self):
        admin = User.objects.create_user(
            email='cateringadmin@example.com',
            password='securepassword1',
            role='admin',
        )
        self.client.force_login(admin)

        response = self.client.post(reverse('delete_meal', args=[self.meal.id]), follow=True)

        self.assertRedirects(response, reverse('admin_panel'))
        self.assertFalse(MealOption.objects.filter(id=self.meal.id).exists())

    def test_admin_can_remove_menu_option_used_by_orders_and_preserve_order(self):
        admin = User.objects.create_user(
            email='cateringadmin@example.com',
            password='securepassword1',
            role='admin',
        )
        order = Order.objects.create(user=self.employee, meal_option=self.meal)
        self.client.force_login(admin)

        listing_response = self.client.get(reverse('admin_panel'))
        self.assertContains(
            listing_response,
            reverse('delete_meal', args=[self.meal.id]),
        )

        response = self.client.post(reverse('delete_meal', args=[self.meal.id]), follow=True)

        self.assertRedirects(response, reverse('admin_panel'))
        self.assertFalse(MealOption.objects.filter(id=self.meal.id).exists())
        order.refresh_from_db()
        self.assertIsNone(order.meal_option)
        self.assertEqual(order.meal_name, self.meal.name)
        self.assertContains(response, f'Selection:</strong> {self.meal.name}')
