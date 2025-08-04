# scripts/seed_admin.py
from users.models import CustomUser

if not CustomUser.objects.filter(username='Admin').exists():
    CustomUser.objects.create_superuser(
        username='Admin',
        email='lotriet.work@gmail.com',
        password='User.1234',
        role='admin'
    )
    print("✅ Admin user created.")
else:
    print("⚠️ Admin user already exists.")
