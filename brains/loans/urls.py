from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, LoanOfferViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loanoffers', LoanOfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
