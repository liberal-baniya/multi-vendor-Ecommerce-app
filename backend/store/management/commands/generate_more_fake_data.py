from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Gallery, Specification, Size, Color, ProductFaq, Product
from userauths.models import User  # Adjust imports as necessary
import random

class Command(BaseCommand):
    help = 'Generate more fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get existing products and users
        products = list(Product.objects.all())
        users = list(User.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please generate products first.'))
            return

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please generate users first.'))
            return

        # Generate Gallery Images
        for _ in range(50):
            Gallery.objects.create(
                product=random.choice(products),
                image=fake.image_url(),
                active=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 gallery images'))

        # Generate Product Specifications
        for _ in range(50):
            Specification.objects.create(
                product=random.choice(products),
                title=fake.word(),
                content=fake.text(max_nb_chars=200),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 specifications'))

        # Generate Product Sizes
        for _ in range(50):
            Size.objects.create(
                product=random.choice(products),
                name=fake.word(),
                price=random.uniform(5.0, 100.0),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 sizes'))

        # Generate Product Colors
        for _ in range(50):
            Color.objects.create(
                product=random.choice(products),
                name=fake.color_name(),
                color_code=fake.hex_color(),
                image=fake.image_url(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 colors'))

        # Generate Product FAQs
        for _ in range(50):
            ProductFaq.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                email=fake.email(),
                question=fake.sentence(),
                answer=fake.text(max_nb_chars=500),
                active=fake.boolean(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 product FAQs'))
