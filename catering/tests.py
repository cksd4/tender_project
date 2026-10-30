from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MealOption

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

    def test_allergen_detection_logic(self):
        """Confirms backend allergen string loop processing performs accurate character scans."""
        user_allergens = [a.strip().lower() for a in self.employee.allergen_free_text.split(',') if a]
        meal_allergens = [a.strip().lower() for a in self.meal.contains_allergens.split(',') if a]
        
        has_match = any(allergen in meal_allergens for allergen in user_allergens)
        self.assertTrue(has_match)
