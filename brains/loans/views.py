from rest_framework import viewsets
from .models import Customer, LoanOffer
from .serializers import GenericModelSerializer

class GenericModelViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = None 

    @classmethod
    def create_for_model(cls, model_class, queryset=None):
        serializer_class = GenericModelSerializer.create_for_model(model_class)
        return type(
            f'{model_class.__name__}ViewSet',
            (cls,),
            {
                'queryset': queryset or model_class.objects.all(),
                'serializer_class': serializer_class
            },
        )

# Creating viewsets dynamically
CustomerViewSet = GenericModelViewSet.create_for_model(Customer)
LoanOfferViewSet = GenericModelViewSet.create_for_model(LoanOffer, queryset=LoanOffer.objects.select_related('customer'))
