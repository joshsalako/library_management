from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, BorrowingViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'borrowings', BorrowingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
