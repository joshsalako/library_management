from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, User, Borrowing
from .serializers import BookSerializer, UserSerializer, BorrowingSerializer
from shared.redis_utils import publish_message

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book = serializer.save()
        publish_message('book_updates', {
            'action': 'create',
            'book_id': book.id,
            'book_data': BookSerializer(book).data
        })

    def perform_destroy(self, instance):
        book_id = instance.id
        instance.delete()
        publish_message('book_updates', {
            'action': 'delete',
            'book_id': book_id
        })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def borrowed_books(self, request, pk=None):
        user = self.get_object()
        borrowings = Borrowing.objects.filter(user=user)
        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data)

class BorrowingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    @action(detail=False, methods=['get'])
    def unavailable_books(self, request):
        unavailable_books = Book.objects.filter(is_available=False)
        serializer = BookSerializer(unavailable_books, many=True)
        return Response(serializer.data)
