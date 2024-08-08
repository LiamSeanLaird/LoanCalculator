# Documentation: Liam

**Note: this is my first time using Django**, I usually use Fast API or ExpressJS.

I used a monorepo because because startups need speed and having full stack engineers with 1 PR per feature helps. 

## Startup instructions: 
x
**Just run `docker-compose up --build` (from the root of the repo)**

1. The backend will generate migration scripts and run them (using an entrypoint.sh file)
2. The API will start up (port 8000)
3. The frontend will start up (port 3000)

The decision to run the migrations on docker-compose is just for demo purposes and not a suggestion for a real product. 

## Django Setup
1. Use django REST framework to use django as purely an API.
2. Use include() in `bank_of_china/urls` url_patterns so I can manage urls in a more modular way.
3. Assume a 1-many relationship between customer and loan offer. As such, a loan offer needs to be linked to a customer
```
class LoanOffer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
```
4. Allow CORS for the frontend to access the API.
5. Run frontend and backend on same network so they can communicate between docker containers

### CRUD + SERIALIZERS
We need serializers to convert models to JSON for REACT (since we aren't using templates). But I don't want to define the columns twice for each model, like this:

```
class LoanOffer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)
    loan_term = models.IntegerField()  # in months
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class LoanOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = ['id', 'customer', 'loan_amount', 'interest_rate', 'loan_term', 'monthly_payment']

class LoanOfferViewSet(viewsets.ModelViewSet):
    queryset = LoanOffer.objects.all()
    serializer_class = LoanOfferSerializer
```

Instead, I use a generic serailizer and generic view set so that I can define the columns in one place. Like this:

```
CustomerViewSet = GenericModelViewSet.create_for_model(LoanOffer)
```

Which is much more scalable. This should give me basic CRUD on my models. 

At this point we can
1. POST /loans/customers
```
curl -X POST http://localhost:8000/loans/customers/ \
     -H 'Content-Type: application/json' \
     -d '{
         "name": "George Hotz",
         "email": "george.hotz@jailbreak.com",
         "bank_balance": "500.00"
     }'

```
2. POST /loans/loanoffers
```
curl -X POST http://localhost:8000/loans/loanoffers/ \
     -H 'Content-Type: application/json' \
     -d '{
         "customer": 1,
         "loan_amount": "10000.00",
         "interest_rate": "5.5",
         "loan_term": 12
     }'
```
3. GET /loans/customers/{id}
```
curl -X GET http://localhost:8000/loans/customers/1/
```

### LOAN CALCULATOR 

Since the monthly payment is dependent on the other loan offer values, it cannot be static. We could calculate on-the-fly when we fetch loan offer information or we could calculate it and save it each time the loan offer is updated. I went for the latter, assuming the loan offer is fetched more than it is updated.

```
class LoanOffer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loan_offers')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2)  # Annual interest rate
    loan_term = models.IntegerField()  # Term in months
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
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
```

### CUSTOM VALIDATION

I think Django handles type validation out-the-box but custom validation for values less than zero for example need to be handled somewhere.

I added this custom validation to the model level. I think it is typically handled in the serializer, but mine is generic. 

Don't really like the validation logic and the fact that the model is becoming cluttered. But I'm running out of time.

This should fail because loan amount is negative:
```
curl -X POST http://localhost:8000/loans/loanoffers/ \
     -H 'Content-Type: application/json' \
     -d '{
         "customer": 1,
         "loan_amount": "-1",
         "interest_rate": "5.5",
         "loan_term": 12
     }'
```

### TESTS

Simple test case for loan payment calc. Also added endpoint test for adding a customer. 

Run this in backend docker container and tests should pass:
```
python manage.py test
```

## React Setup 

### Component design

1. Have the LoanPage component at the top of the tree with LoanDisplay to render the loan info and LoanForm to accept user inputs.
2. Use useState and an update hook to define the loan info on the loan page and update this info in the loanForm. 

Following the *principle of uncontrolled components* - both LoanForm nd LoanDisplay can be used to capture and display loan information elsewhere in the app if need be. 

### Handling CSS

Using inline css like tailwind paired with prebuilt components like bootstrap reduces code written & maintained. This is usually a good tradeoff for startups.

Implemented tailwind:
```
<form className="flex-row" onSubmit={handleSubmit}>
    ...
</form>
```

### Testing

1. Put `LoanForm.test.ts` in the same directory as the component for maintainability. Just had to edit the jest config to recognize the test. 
2. Simple UI render test for `LoanForm`

Run this in frontend container:
```
npm run test
```

I could also add tests on the input validation and form submission to improve test coverage















