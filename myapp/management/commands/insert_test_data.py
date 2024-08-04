from django.core.management.base import BaseCommand
from myapp.models import User, BlockList

class Command(BaseCommand):
    help = 'Insert test data into the database'

    def handle(self, *args, **kwargs):
        user1 = User.objects.create(
            user_name='Alice123',
            passwd='securePass123',
            email='alice@example.com'
            # email_code='123456'
        )

        user2 = User.objects.create(
            user_name='Bob456',
            passwd='securePass456',
            email='bob@example.com'
            # email_code='654321'
        )

        user3 = User.objects.create(
            user_name='Charlie789',
            passwd='securePass789',
            email='charlie@example.com'
            # email_code='789012'
        )

        user1.is_active = True
        user1.email_code = ''
        user1.save()

        user2.is_active = True
        user2.email_code = ''
        user2.save()

        user3.is_active = True
        user3.email_code = ''
        user3.save()

        BlockList.objects.create(from_user=user1, to_user=user2)
        BlockList.objects.create(from_user=user1, to_user=user3)
        BlockList.objects.create(from_user=user2, to_user=user3)

        self.stdout.write(self.style.SUCCESS('Successfully inserted test data'))
