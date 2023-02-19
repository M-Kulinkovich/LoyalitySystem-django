from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.utils import timezone


class Cards(models.Model):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = 'EXPIRED'
    STATUS = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (EXPIRED, 'Expired')
    ]
    series_card = models.CharField(max_length=1)
    number_card = models.IntegerField()
    status_card = models.CharField(choices=STATUS, default=ACTIVE, max_length=10)
    create_date_card = models.DateTimeField()
    ending_date_card = models.DateTimeField()
    last_activity_card = models.DateTimeField(auto_now=True)
    amount_purchase = models.FloatField(default=0)
    discount_percent = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])


    def update_status(self):
        if self.ending_date_card < timezone.now():
            self.status_card = self.EXPIRED
            self.save()


    def __str__(self):
        return f'{self.series_card}{self.number_card} | status: {self.status_card} | discount {self.discount_percent}% amount purchase {self.amount_purchase}$:'

    class Meta:
        verbose_name = "Cards"
        verbose_name_plural = "Card"


class Orders(models.Model):
    card_id = models.ForeignKey(Cards, on_delete=models.CASCADE, related_name='orders')
    date_order = models.DateTimeField(auto_now_add=True)
    sum_order = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'N{self.id} |Discount sum: {self.discount}$ | discount: {self.discount_percent}%'

    def save(self, *args, **kwargs):
        discount_percent_orders = self.card_id.discount_percent
        self.discount_percent = discount_percent_orders
        super(Orders, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Order"


def update_cards(sender, instance, **kwargs):
        card = instance.card_id
        if card is not None:
            card.amount_purchase = sum([orders.discount for orders in card.orders.all()])
            card.save()


post_save.connect(update_cards, sender=Orders)


class Product(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=128, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(default=0)

    def __str__(self):
        return f'order N{self.order.id} ||{self.name} - {self.price}$ | discount_prise: {self.discount_price}$'

    def save(self, *args, **kwargs):
        discount_price_product = self.order.discount_percent
        self.discount_price = self.price - (self.price * discount_price_product * 0.01)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Product"


def update_order(sender, instance, **kwargs):
        order = instance.order
        if order is not None:
            order.sum_order = sum([product.price for product in order.products.all()])
            order.discount = sum([product.discount_price for product in order.products.all()])
            order.save()

post_save.connect(update_order, sender=Product)








