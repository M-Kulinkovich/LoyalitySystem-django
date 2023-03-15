from django.test import TestCase
from polls.models import Cards, Orders, Product
from django.core.exceptions import ValidationError


class Settings(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cards = Cards.objects.create(
            series_card='A',
            number_card=55555,
            status_card='ACTIVE',
            create_date_card='2023-03-15 13:10:44.943184+00',
            ending_date_card='2023-03-15 15:10:44.943184+00',
            amount_purchase=123,
            discount_percent=15,
        )


class TestModelsCards(Settings):

    def test_series_card_label(self):
        name_field = self.cards._meta.get_field('series_card')
        self.assertEqual(name_field.verbose_name, 'Серия карты')
        self.assertEqual(name_field.max_length, 1)

    def test_number_card_label(self):
        name_field = self.cards._meta.get_field('number_card')
        self.assertEquals(name_field.verbose_name, 'Номер карты')

    def test_status_card_label(self):
        name_field = self.cards._meta.get_field('status_card')
        self.assertEquals(name_field.verbose_name, 'Статус карты')
        self.assertEquals(name_field.max_length, 10)
        self.assertEqual(name_field.default, 'ACTIVE')

    def test_create_date_card_label(self):
        name_field = self.cards._meta.get_field('create_date_card')
        self.assertEquals(name_field.verbose_name, 'Дата создания карты')

    def test_ending_date_card_label(self):
        name_field = self.cards._meta.get_field('ending_date_card')
        self.assertEquals(name_field.verbose_name, 'Дата окончания карты')

    def test_last_activity_card_label(self):
        name_field = self.cards._meta.get_field('last_activity_card')
        self.assertEquals(name_field.verbose_name, 'Последняя активность карты')

    def test_amount_purchase_label(self):
        name_field = self.cards._meta.get_field('amount_purchase')
        self.assertEquals(name_field.verbose_name, 'Общая сумма покупок по карте')
        self.assertEqual(name_field.default, 0)

    def test_discount_percent_label(self):
        name_field = self.cards._meta.get_field('discount_percent')
        self.assertEquals(name_field.verbose_name, 'Скидка')
        self.assertEqual(name_field.default, 1)
        self.assertEqual(name_field.validators[0].limit_value, 0)

    def test_validators_value_fail(self):
        invalid_value = Cards(discount_percent=121)
        with self.assertRaises(ValidationError):
            invalid_value.full_clean()
            invalid_value.save()

    def test_string_representation(self):
        self.assertEqual(str(self.cards), 'A55555 | status: ACTIVE | discount 15% amount purchase 123$')


# class TestModelsOrders(TestCase):
# class TestModelsProducts(TestCase):