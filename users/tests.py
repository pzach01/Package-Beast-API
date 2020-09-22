from django.test import TestCase
'''
# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class UserTests(APITestCase):
    def test_create_and_read_user(self):
        """
        Ensure we can create a new user object.
        """
        u = User.objects.create(email='a@a.com')
        u.set_password('a')
        u.save()
        # url = reverse('account-list')
        self.client.login(email="a@a.com", password="a")

        url = '/users/1/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'a@a.com')
        print("Passed User Test 1")
'''