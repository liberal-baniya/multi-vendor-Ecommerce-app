from django.core.management.base import BaseCommand
from faker import Faker
from store.models import CancelledOrder, CouponUsers, DeliveryCouriers, User, Coupon, CartOrder, CartOrderItem  # Adjust imports as necessary
import random

class Command(BaseCommand):
    help = 'Generate fake data for miscellaneous models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = list(User.objects.all())
        coupons = list(Coupon.objects.all())
        cart_orders = list(CartOrder.objects.all())
        cart_order_items = list(CartOrderItem.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please generate users first.'))
            return

        if not coupons:
            self.stdout.write(self.style.ERROR('No coupons found. Please generate coupons first.'))
            return

        if not cart_orders:
            self.stdout.write(self.style.ERROR('No cart orders found. Please generate cart orders first.'))
            return

        if not cart_order_items:
            self.stdout.write(self.style.ERROR('No cart order items found. Please generate cart order items first.'))
            return

        # Generate CancelledOrders
        for _ in range(30):
            CancelledOrder.objects.create(
                user=random.choice(users),
                orderitem=random.choice(cart_order_items),
                email=fake.email(),
                refunded=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 30 cancelled orders'))

        # Generate CouponUsers
        for _ in range(30):
            CouponUsers.objects.create(
                coupon=random.choice(coupons),
                order=random.choice(cart_orders),
                full_name=fake.name(),
                email=fake.email(),
                mobile=fake.phone_number(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 30 coupon users'))

        # Generate DeliveryCouriers
        for _ in range(15):
            DeliveryCouriers.objects.create(
                name=fake.company(),
                tracking_website=fake.url(),
                url_parameter=fake.slug(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 15 delivery couriers'))
