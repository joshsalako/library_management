import os
os.environ['TEST'] = 'True'

from django.test import TestCase
from rest_framework.test import APIClient
from .models import Book, User, Borrowing
from django.utils import timezone
from datetime import timedelta

class AdminAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', firstname='Test', lastname='User')
        self.book = Book.objects.create(title='Test Book', author='Test Author', publisher='Test Publisher', category='Test Category')

    def test_add_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publisher': 'New Publisher',
            'category': 'New Category'
        }
        response = self.client.post('/api/admin/books/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_remove_book(self):
        response = self.client.delete(f'/api/admin/books/{self.book.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    def test_list_users(self):
        response = self.client.get('/api/admin/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_user_borrowed_books(self):
        Borrowing.objects.create(user=self.user, book=self.book, return_date=timezone.now().date() + timedelta(days=7))
        response = self.client.get(f'/api/admin/users/{self.user.id}/borrowed_books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book']['title'], 'Test Book')

    def test_unavailable_books(self):
        self.book.is_available = False
        self.book.save()
        response = self.client.get('/api/admin/borrowings/unavailable_books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')
