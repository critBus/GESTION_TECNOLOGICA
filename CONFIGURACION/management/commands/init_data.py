import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from seed_data import run_seed
User = get_user_model()
def creat_first_superuser_and_roles():
    
    
    User.objects.create_superuser(
        username="admin",
        email="admin@gmail.com",
        first_name="admin",
        last_name="admin",
        password="123",
    )
        



class Command(BaseCommand):
    help = "Create All Tables"

    def handle(self, *args, **kwargs):
        try:
            if User.objects.all().count() == 0:
                creat_first_superuser_and_roles()
                run_seed()

        except Exception:
            print(traceback.format_exc())
