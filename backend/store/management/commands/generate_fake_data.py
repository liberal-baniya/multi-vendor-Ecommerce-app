from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Category, Tag, Brand, Product
from userauths.models import User# Adjust imports as necessary
from vendor.models import Vendor
import random


class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate Users
        users = []
        for _ in range(10):
            email = fake.unique.email()
            username = email.split('@')[0]
            user = User.objects.create_user(
                username=username,
                email=email,
                full_name=fake.name(),
                phone=fake.phone_number(),
                otp=fake.random_number(digits=6, fix_len=True),
                reset_token=fake.uuid4(),
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 users'))

        # Generate Categories
        categories = []
        for _ in range(10):
            category = Category.objects.create(
                title=fake.word(),
                slug=fake.slug(),
                active=fake.boolean(),
            )
            categories.append(category)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 categories'))

        # Generate Tags
        for _ in range(20):
            Tag.objects.create(
                title=fake.word(),
                category=random.choice(categories),
                active=fake.boolean(),
                slug=fake.slug(),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created 20 tags'))

        # Generate Brands
        brands = []
        for _ in range(10):
            brand = Brand.objects.create(
                title=fake.company(),
                active=fake.boolean(),
            )
            brands.append(brand)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 brands'))

        # Generate Vendors
        available_users = list(users)  # Create a copy of the users list to ensure unique assignment
        vendors = []
        for _ in range(10):
            if available_users:  # Ensure there are available users left
                user = available_users.pop(0)  # Get a unique user
                vendor = Vendor.objects.create(
                    user=user,
                    name=fake.company(),
                    email=fake.company_email(),
                    description=fake.text(),
                    mobile=fake.phone_number(),
                    verified=fake.boolean(),
                    active=fake.boolean(),
                    slug=fake.slug(),
                )
                vendors.append(vendor)

        self.stdout.write(self.style.SUCCESS(f'Successfully created 10 vendors'))

        # Generate Products
        for _ in range(50):
            Product.objects.create(
                title=fake.word(),
                description=fake.text(),
                category=random.choice(categories),
                tags=fake.words(3, unique=True),
                brand=random.choice(brands).title,
                price=random.uniform(10.0, 100.0),
                old_price=random.uniform(10.0, 100.0),
                shipping_amount=random.uniform(5.0, 15.0),
                stock_qty=random.randint(0, 100),
                in_stock=fake.boolean(),
                status=random.choice(['draft', 'disabled', 'rejected', 'in_review', 'published']),
                type=random.choice(['regular', 'auction', 'offer']),
                featured=fake.boolean(),
                hot_deal=fake.boolean(),
                special_offer=fake.boolean(),
                digital=fake.boolean(),
                views=random.randint(0, 1000),
                orders=random.randint(0, 100),
                saved=random.randint(0, 100),
                rating=random.randint(1, 5),
                vendor=random.choice(vendors),
                sku=fake.unique.bothify(text='SKU-#####'),
                pid=fake.unique.bothify(text='??####'),
                slug=fake.slug(),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created 50 products'))
