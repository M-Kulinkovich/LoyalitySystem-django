from django.test import TestCase
from django.urls import reverse, resolve
from polls.views import index_page, remote_cards_page, generate_cards_page, cards_info


class TestLoyalityUrl(TestCase):

    def test_index_page(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index_page)

    def test_remote_page(self):
        url = reverse('remote_cards')
        self.assertEqual(resolve(url).func, remote_cards_page)

    def test_generate_page(self):
        url = reverse('generate_cards')
        self.assertEqual(resolve(url).func, generate_cards_page)

    def test_cards_page(self):
        url = reverse('cards_info', args=['1'])
        self.assertEqual(resolve(url).func, cards_info)

