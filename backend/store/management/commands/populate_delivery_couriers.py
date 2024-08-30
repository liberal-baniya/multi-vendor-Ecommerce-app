from django.core.management.base import BaseCommand
from store.models import CartOrderItem, DeliveryCouriers  # Adjust imports as necessary
import random

class Command(BaseCommand):
    help = 'Populate delivery couriers for existing cart order items'

    def handle(self, *args, **kwargs):
        delivery_couriers = list(DeliveryCouriers.objects.all())

        if not delivery_couriers:
            self.stdout.write(self.style.ERROR('No delivery couriers found. Please generate delivery couriers first.'))
            return

        cart_order_items = CartOrderItem.objects.filter(delivery_couriers__isnull=True)

        if not cart_order_items.exists():
            self.stdout.write(self.style.WARNING('No cart order items found without delivery couriers.'))
            return

        for item in cart_order_items:
            item.delivery_couriers = random.choice(delivery_couriers)
            item.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated delivery couriers for {cart_order_items.count()} cart order items'))
