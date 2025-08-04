from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Seeds the database with a default admin user'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='Admin').exists():
            CustomUser.objects.create_superuser(
                username='Admin',
                email='lotriet.work@gmail.com',
                password='User.1234',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('✅ Admin user created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin user already exists.'))
