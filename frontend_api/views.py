from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import User, Book, Borrowing
from .serializers import UserSerializer, BookSerializer, BorrowingSerializer, UserEnrollmentSerializer
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        serializer = UserEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        publisher = self.request.query_params.get('publisher')
        category = self.request.query_params.get('category')
        
        if publisher:
            queryset = queryset.filter(publisher=publisher)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')
        days = request.data.get('days', 14)

        if not book.is_available:
            return Response({"error": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            return_date = timezone.now().date() + timedelta(days=int(days))
            borrowing = Borrowing.objects.create(user=user, book=book, return_date=return_date)
            
            book.is_available = False
            book.available_from = return_date
            book.save()

            logger.info(f"Book {book.id} borrowed by user {user.id}")
            return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in borrow action: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

