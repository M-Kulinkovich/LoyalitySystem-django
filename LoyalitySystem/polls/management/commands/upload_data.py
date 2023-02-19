import random
import string
from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand
from polls.models import Cards, Orders, Product


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **options):
            # Создание 5 карт
            for i in range(5):
                card = Cards(
                    series_card=random.choice(string.ascii_letters).upper(),
                    number_card=random.randint(10000, 99999),
                    status_card=random.choice([Cards.ACTIVE, Cards.INACTIVE]),
                    create_date_card=timezone.now() - timedelta(days=random.randint(1, 30)),
                    ending_date_card=timezone.now() + timedelta(days=random.randint(1, 30)),
                    amount_purchase=0,
                    discount_percent=random.randint(0, 50)
                )
                card.save()

                # Для каждой карты создаем 1-3 заказов
                for j in range(random.randint(1, 3)):
                    order = Orders(
                        card_id=card,
                        date_order=timezone.now() - timedelta(days=random.randint(1, 30)),
                        discount_percent=0
                    )
                    order.save()

                    # Для каждого заказа создаем 1-5 продуктов
                    for k in range(random.randint(1, 5)):
                        product = Product(
                            order=order,
                            name=f'продукт номер {k + 1}',
                            price=random.uniform(10, 100)
                        )
                        product.save()
    print("данные добавлены в бд")






