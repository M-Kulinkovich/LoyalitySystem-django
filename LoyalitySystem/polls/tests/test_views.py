from django.test import TestCase, Client
from django.urls import reverse
from polls.models import Cards


class TestLoyalityViews(TestCase):

    def test_index_GET(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_generate_GET(self):
        response = self.client.get('/generate/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generateCard.html')

    def test_remote_GET(self):
        response = self.client.get('/remote/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'remoteCard.html')

    def test_generate_POST_with_data(self):
        response = self.client.post('/generate/', {
            'series_card': 'B',
            'number_card': 7777,
            'create_date_card': '2023-03-15 11:10:44.943184+00',
            'ending_date_card': '2023-03-15 19:12:44.943184+00',
        })
        latest_cards = Cards.objects.latest('id')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(latest_cards.series_card, 'B')

    def test_cards_info(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bonusCard.html')

