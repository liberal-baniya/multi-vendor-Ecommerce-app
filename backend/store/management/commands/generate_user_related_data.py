from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Review, Wishlist, Notification, Address, Product, CartOrder, CartOrderItem  # Adjust imports as necessary
import random
from userauths.models import User  # Adjust imports as necessary
from vendor.models import Vendor
from addon.models import Tax

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class Command(BaseCommand):
    help = 'Generate fake user-related data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing objects
        products = list(Product.objects.all())
        users = list(User.objects.all())
        vendors = list(Vendor.objects.all())
        cart_orders = list(CartOrder.objects.all())
        cart_order_items = list(CartOrderItem.objects.all())

        # Check for necessary data
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please generate products first.'))
            return

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please generate users first.'))
            return

        if not vendors:
            self.stdout.write(self.style.ERROR('No vendors found. Please generate vendors first.'))
            return

        if not cart_orders:
            self.stdout.write(self.style.ERROR('No cart orders found. Please generate cart orders first.'))
            return

        if not cart_order_items:
            self.stdout.write(self.style.ERROR('No cart order items found. Please generate cart order items first.'))
            return

        # Generate Reviews
        for _ in range(50):
            review = Review.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                review=fake.text(max_nb_chars=500),
                reply=fake.sentence() if random.choice([True, False]) else None,
                rating=random.choice([rating[0] for rating in RATING]),
                active=fake.boolean(),
            )
            review.helpful.set(random.sample(users, random.randint(0, 10)))
            review.not_helpful.set(random.sample(users, random.randint(0, 5)))

        self.stdout.write(self.style.SUCCESS('Successfully created 50 reviews'))

        # Generate Wishlists
        for _ in range(50):
            Wishlist.objects.create(
                user=random.choice(users),
                product=random.choice(products),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 wishlists'))

        # Generate Notifications
        for _ in range(50):
            Notification.objects.create(
                user=random.choice(users),
                vendor=random.choice(vendors),
                order=random.choice(cart_orders),
                order_item=random.choice(cart_order_items),
                seen=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 notifications'))

        # Generate Taxes
        for _ in range(20):
            Tax.objects.create(
                country=fake.country(),
                rate=random.randint(5, 20),
                active=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 20 taxes'))

        # Fetch the newly created taxes
        taxes = list(Tax.objects.all())

        # Generate Addresses
        for _ in range(50):
            Address.objects.create(
                user=random.choice(users),
                full_name=fake.name(),
                mobile=fake.phone_number(),
                email=fake.email(),
                country=random.choice(taxes) if taxes else None,
                state=fake.state(),
                town_city=fake.city(),
                address=fake.street_address(),
                zip=fake.zipcode(),
                status=fake.boolean(),
                same_as_billing_address=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 addresses'))
