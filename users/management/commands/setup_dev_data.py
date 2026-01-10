from django.core.management.base import BaseCommand
from users.models import User
from shops.models import Shops

class Command(BaseCommand):
    help = 'Creates initial development data: One Superuser, One Seller, and One Standard User.'

    def get_unique_username(self, email):
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def handle(self, *args, **options):
        # 1. Create Superuser
        admin_email = 'admin@example.com'
        if not User.objects.filter(email=admin_email).exists():
            username = 'admin'
            if User.objects.filter(username=username).exists():
                username = self.get_unique_username(admin_email)
            
            User.objects.create_superuser(
                email=admin_email,
                username=username,
                password='adminpassword',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {admin_email} (Username: {username})'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {admin_email} already exists.'))

        # 2. Create Standard User
        user_email = 'user@example.com'
        if not User.objects.filter(email=user_email).exists():
            username = self.get_unique_username(user_email)
            User.objects.create_user(
                email=user_email,
                username=username,
                password='password123',
                first_name='John',
                last_name='Doe'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created standard user: {user_email} (Username: {username})'))
        else:
            self.stdout.write(self.style.WARNING(f'Standard user {user_email} already exists.'))

        # 3. Create Seller
        seller_email = 'seller@example.com'
        shop_name = 'Dev Shop'
        if not User.objects.filter(email=seller_email).exists():
            username = self.get_unique_username(seller_email)
            seller = User.objects.create_vendor(
                email=seller_email,
                username=username,
                password='password123',
                shop_name=shop_name,
                first_name='Jane',
                last_name='Seller'
            )
            
            # Create the Shop object
            Shops.objects.create(
                user=seller,
                name=shop_name,
                description='This is a default development shop.'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created seller: {seller_email} (Username: {username}) and shop: {shop_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Seller {seller_email} already exists.'))
