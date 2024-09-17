import os
os.environ['TEST'] = 'True'

from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Book, Borrowing
from django.utils import timezone
from datetime import timedelta

class FrontendAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', firstname='Test', lastname='User')
        self.book = Book.objects.create(title='Test Book', author='Test Author', publisher='Test Publisher', category='Test Category')

    def test_user_enrollment(self):
        data = {'email': 'new@example.com', 'firstname': 'New', 'lastname': 'User'}
        response = self.client.post('/api/frontend/users/enroll/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)

    def test_book_list(self):
        response = self.client.get('/api/frontend/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_book_filter(self):
        Book.objects.create(title='Another Book', author='Another Author', publisher='Another Publisher', category='Another Category')
        response = self.client.get('/api/frontend/books/', {'publisher': 'Test Publisher'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    def test_book_borrow(self):
        data = {'user_id': self.user.id, 'days': 7}
        response = self.client.post(f'/api/frontend/books/{self.book.id}/borrow/', data)
        self.assertEqual(response.status_code, 201)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)
        self.assertEqual(Borrowing.objects.count(), 1)

    def test_borrow_unavailable_book(self):
        self.book.is_available = False
        self.book.save()
        data = {'user_id': self.user.id, 'days': 7}
        response = self.client.post(f'/api/frontend/books/{self.book.id}/borrow/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Book is not available")

    def test_borrow_nonexistent_book(self):
        data = {'user_id': self.user.id, 'days': 7}
        response = self.client.post('/api/frontend/books/9999/borrow/', data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], "Book not found")
