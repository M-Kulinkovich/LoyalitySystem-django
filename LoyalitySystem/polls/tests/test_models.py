from django.test import TestCase
from polls.models import Cards, Orders, Product
from django.core.exceptions import ValidationError


class Settings(TestCase):

    def setUp(self):
        self.cards = Cards.objects.create(
            series_card='A',
            number_card=55555,
            status_card='ACTIVE',
            create_date_card='2023-03-15 13:10:44.943184+00',
            ending_date_card='2023-03-15 15:10:44.943184+00',
            amount_purchase=9,
            discount_percent=10,
        )

        self.orders = Orders.objects.create(
            card_id=self.cards,
            date_order='2023-03-16 11:10:44.943184+00',
            sum_order=10,
            discount_percent=10,
            discount=9,
        )

        orders2 = Orders.objects.create(
            card_id=self.cards,
            date_order='2023-03-16 11:10:44.943184+00',
            sum_order=100,
            discount_percent=15,
            discount=15,
        )

        self.products = Product.objects.create(
            order=self.orders,
            name='Молоко',
            price=10,
            discount_price=9
        )

        products2 = Product.objects.create(
            order=self.orders,
            name='Хлеб',
            price=5,
            discount_price=4.5
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


class TestModelsOrders(Settings):

    def test_validators(self):
        name_field = self.orders._meta.get_field('discount_percent')
        self.assertEqual(name_field.validators[0].limit_value, 0)

    def test_validators_value_fail(self):
        invalid_value = Orders(discount_percent=155)
        with self.assertRaises(ValidationError):
            invalid_value.full_clean()
            invalid_value.save()

    def test_discount(self):
        self.assertEqual(self.orders.sum_order, 13.5)

    def test_discount_percent(self):
        self.assertEqual(self.orders.discount_percent, self.cards.discount_percent)

    def test_update_cards(self):
        self.assertEqual(self.cards.amount_purchase, 113.5)


class TestModelsProducts(Settings):

    def test_discount_price(self):
        self.assertEqual(self.products.discount_price, 9)

    def test_update_orders(self):
        self.assertEqual(self.orders.sum_order, 13.5)