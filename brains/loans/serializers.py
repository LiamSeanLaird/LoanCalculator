from rest_framework import serializers
from .models import Customer, LoanOffer

class GenericModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None # This is set by create_for_model

    @classmethod
    def create_for_model(cls, model_class):
        class Meta:
            model = model_class
            fields = '__all__'
        attrs = {'Meta': Meta}
        
        if hasattr(model_class, 'validate'):
            for field_name, validator in model_class.validate.items():
                method_name = f'validate_{field_name}'
                if not hasattr(cls, method_name):
                    setattr(cls, method_name, validator)
                
        return type(f'{model_class.__name__}Serializer', (cls,), attrs)