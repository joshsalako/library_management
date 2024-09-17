from django.core.management.base import BaseCommand
from shared.redis_utils import subscribe_to_channel
from frontend_api.models import Book
import json

class Command(BaseCommand):
    help = 'Runs the Redis subscriber for book updates'

    def handle(self, *args, **options):
        self.stdout.write('Starting Redis subscriber...')
        pubsub = subscribe_to_channel('book_updates')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                self.process_message(data)

    def process_message(self, data):
        action = data['action']
        book_id = data['book_id']

        if action == 'create':
            book_data = data['book_data']
            Book.objects.create(**book_data)
            self.stdout.write(f'Created book: {book_data["title"]}')
        elif action == 'delete':
            Book.objects.filter(id=book_id).delete()
            self.stdout.write(f'Deleted book with id: {book_id}')
