"""
Tests for recipe APIs.
"""
from decimal import Decimal

ffrom django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """Create a recipe."""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe =  Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test the authenticaiton is required"""
        res = self.client.post(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(self.user)
        create_recipe(self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'user2@example.com',
            'testpass123',
        )
        create_recipe(user=user2)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recepies = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recepies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)