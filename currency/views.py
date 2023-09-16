from django.http import JsonResponse
from rest_framework.decorators import api_view

from currency.models import CurrencyModel
from currency.serializers import CurrencySerializer


#
@api_view(["GET"])
def currency_data_view(request):
    queryset = CurrencyModel.objects.all().first()
    serializer = CurrencySerializer(queryset)
    return JsonResponse({"data": serializer.data})
