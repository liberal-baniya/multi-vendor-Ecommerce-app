from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Coupon, Cart, CartOrder, CartOrderItem, Product
from userauths.models import User  # Adjust imports as necessary
from vendor.models import Vendor
import random

DELIVERY_STATUS = (
    ("On Hold", "On Hold"),
    ("Shipping Processing", "Shipping Processing"),
    ("Shipped", "Shipped"),
    ("Arrived", "Arrived"),
    ("Delivered", "Delivered"),
    ("Returning", "Returning"),
    ("Returned", "Returned"),
)
PAYMENT_STATUS = (
    ("paid", "Paid"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("cancelled", "Cancelled"),
    ("initiated", "Initiated"),
    ("failed", "failed"),
    ("refunding", "refunding"),
    ("refunded", "refunded"),
    ("unpaid", "unpaid"),
    ("expired", "expired"),
)


ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Fulfilled", "Fulfilled"),
    ("Partially Fulfilled", "Partially Fulfilled"),
    ("Cancelled", "Cancelled"),
)


class Command(BaseCommand):
    help = "Generate fake order data for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()

        products = list(Product.objects.all())
        users = list(User.objects.all())
        vendors = list(Vendor.objects.all())

        if not products:
            self.stdout.write(
                self.style.ERROR("No products found. Please generate products first.")
            )
            return

        if not users:
            self.stdout.write(
                self.style.ERROR("No users found. Please generate users first.")
            )
            return

        if not vendors:
            self.stdout.write(
                self.style.ERROR("No vendors found. Please generate vendors first.")
            )
            return

        # Generate Coupons
        coupons = []
        for _ in range(20):
            coupon = Coupon.objects.create(
                vendor=random.choice(vendors),
                code=fake.unique.lexify(text="COUPON-?????"),
                discount=random.randint(5, 50),
                active=fake.boolean(),
            )
            coupon.used_by.set(random.sample(users, random.randint(0, 5)))
            coupons.append(coupon)

        self.stdout.write(self.style.SUCCESS("Successfully created 20 coupons"))

        # Generate Carts
        carts = []
        for _ in range(50):
            cart = Cart.objects.create(
                product=random.choice(products),
                user=random.choice(users),
                qty=random.randint(1, 5),
                price=random.uniform(10.0, 100.0),
                sub_total=random.uniform(10.0, 500.0),
                shipping_amount=random.uniform(5.0, 20.0),
                service_fee=random.uniform(1.0, 10.0),
                tax_fee=random.uniform(2.0, 15.0),
                total=random.uniform(20.0, 600.0),
                country=fake.country(),
                size=fake.word(),
                color=fake.color_name(),
                cart_id=fake.unique.lexify(text="CART-?????"),
            )
            carts.append(cart)

        self.stdout.write(self.style.SUCCESS("Successfully created 50 carts"))

        # Generate Cart Orders
        cart_orders = []
        for _ in range(20):
            cart_order = CartOrder.objects.create(
                buyer=random.choice(users),
                sub_total=random.uniform(100.0, 1000.0),
                shipping_amount=random.uniform(10.0, 50.0),
                tax_fee=random.uniform(10.0, 100.0),
                service_fee=random.uniform(5.0, 25.0),
                total=random.uniform(150.0, 1200.0),
                payment_status=random.choice(
                    [status[0] for status in PAYMENT_STATUS]
                ),  # Updated here
                order_status=random.choice(
                    [status[0] for status in ORDER_STATUS]
                ),  # Updated here
                initial_total=random.uniform(150.0, 1300.0),
                saved=random.uniform(10.0, 100.0),
                full_name=fake.name(),
                email=fake.email(),
                mobile=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country(),
                stripe_session_id=fake.uuid4(),
            )
            cart_order.vendor.set(random.sample(vendors, random.randint(1, 3)))
            cart_order.coupons.set(random.sample(coupons, random.randint(0, 2)))
            cart_orders.append(cart_order)

        self.stdout.write(self.style.SUCCESS("Successfully created 20 cart orders"))

        # Generate Cart Order Items
        for _ in range(50):
            CartOrderItem.objects.create(
                order=random.choice(cart_orders),
                product=random.choice(products),
                qty=random.randint(1, 5),
                price=random.uniform(10.0, 200.0),
                sub_total=random.uniform(50.0, 1000.0),
                shipping_amount=random.uniform(5.0, 30.0),
                tax_fee=random.uniform(5.0, 25.0),
                service_fee=random.uniform(2.0, 15.0),
                total=random.uniform(100.0, 1200.0),
                color=fake.color_name(),
                size=fake.word(),
                delivery_status=random.choice(
                    [status[0] for status in DELIVERY_STATUS]
                ),  # Updated here
                tracking_id=fake.unique.lexify(text="TRACK-?????"),
                vendor=random.choice(vendors),
                applied_coupon=fake.boolean(),
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully created 50 cart order items")
        )
