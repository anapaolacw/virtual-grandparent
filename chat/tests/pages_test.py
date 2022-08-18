from django.test import TestCase

# Create your tests here.
class URLTests(TestCase):
    # Tests all urls
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_helper_menu_page(self):
        response = self.client.get('/helper/menu/')
        self.assertEqual(response.status_code, 200)

    def test_help_requests_page(self):
        response = self.client.get('help-requests/')
        self.assertEqual(response.status_code, 200)

    def test_all_help_requests_page(self):
        response = self.client.get('help-requests/all/')
        self.assertEqual(response.status_code, 200)

    def test_create_help_request_page(self):
        response = self.client.get('help-request/create/')
        self.assertEqual(response.status_code, 200)

    # def test_edit_help_request_page(self):
    #     response = self.client.get('help-request/edit/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_help_request_page(self):
    #     response = self.client.get('help-request/delete/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_create_help_offer_page(self):
    #     response = self.client.get('help-offer/create/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_help_request_candidates_page(self):
    #     response = self.client.get('help-request/candidates/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_accept_candidate_page(self):
    #     response = self.client.get('help-request/candidate/acept/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_offer_help_page(self):
    #     response = self.client.get('my-offer-help/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_offers_page(self):
    #     response = self.client.get('my-offers')
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_offer_page(self):
    #     response = self.client.get('my-offer/delete/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_offer_page(self):
    #     response = self.client.get('my-offer/edit/<int:id>')
    #     self.assertEqual(response.status_code, 200)

    