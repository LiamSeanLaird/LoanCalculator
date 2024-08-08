from django.db import models
import math
from django.core.exceptions import ValidationError

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=100)

class LoanOffer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loan_offers', null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)  # Annual interest rate
    loan_term = models.IntegerField()  # Term in months
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.clean()
        self.monthly_payment = self.calculate_monthly_payment()
        super().save(*args, **kwargs)

    def calculate_monthly_payment(self):
        loan_amount = float(self.loan_amount)
        loan_term = float(self.loan_term)
        interest_rate = float(self.interest_rate)
        if self.interest_rate == 0:
            return loan_amount / loan_term

        monthly_interest_rate = (interest_rate / 100) / 12
        number_of_payments = loan_term
        monthly_payment = (
            loan_amount *
            monthly_interest_rate *
            math.pow((1 + monthly_interest_rate), number_of_payments)
        ) / (math.pow((1 + monthly_interest_rate), number_of_payments) - 1)

        return round(monthly_payment, 2)
    
    def clean(self):
        if self.loan_amount <= 0:
            raise ValidationError({'loan_amount': 'must be greater than zero.'})
        if self.interest_rate < 0:
            raise ValidationError({'interest_rate': 'cannot be negative.'})
        if self.loan_term <= 0:
            raise ValidationError({'loan_term': 'must be greater than zero.'})