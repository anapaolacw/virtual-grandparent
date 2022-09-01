from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class URLTests(TestCase):
    # Tests all urls
    def test_register_page(self):
        url = reverse('authentication:signup', args=("helper",))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        url = reverse('authentication:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
