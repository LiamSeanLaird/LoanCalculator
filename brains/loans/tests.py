from django.test import TestCase
from .models import Customer, LoanOffer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LoanOfferTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="GH", email="g@h.jb", bank_balance=1000)

    def test_loan_payment_calculation(self):
        loan_offer = LoanOffer(customer=self.customer, loan_amount=1000, interest_rate=10, loan_term=12)
        loan_offer.save()
        self.assertAlmostEqual(loan_offer.monthly_payment, 87.92)

class CustomerCreationTestCase(APITestCase):
    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            "name": "George Hotz",
            "email": "george.hotz@jailbreak.com",
            "bank_balance": "500.00"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, 'George Hotz')
        self.assertEqual(Customer.objects.get().email, 'george.hotz@jailbreak.com')
        self.assertEqual(float(Customer.objects.get().bank_balance), 500.00)
