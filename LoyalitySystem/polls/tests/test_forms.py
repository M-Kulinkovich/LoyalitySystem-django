from django.test import TestCase
from polls.forms import CardsForm


class TestLoyalityForms(TestCase):

    def test_form_valid_data(self):
        form = CardsForm(data={
            'series_card': 'A',
            'number_card': 55555,
            'create_date_card': '2023-03-15 13:10:44.943184+00',
            'ending_date_card': '2023-03-15 15:10:44.943184+00',
        })

        self.assertTrue(form.is_valid())

    def test_form_without_data(self):
        form = CardsForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
