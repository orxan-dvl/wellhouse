from currency.models import CurrencyModel
from rest_framework.serializers import ModelSerializer

#
class CurrencySerializer(ModelSerializer):
    class Meta:
        model = CurrencyModel
        fields = '__all__'