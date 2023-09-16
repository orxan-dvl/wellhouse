from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import APIException

from services.modelserializers import (PostSaleServiceFormSerializer, ServicemodelSerializer,
                                       ApartmentExchangeFormSerializer, FinishingChoiceSerializer)
from services.models import Servicemodel

from services.serializers import (OrientationFormSerializer, ConsultingFormSerializer, OnlineVisitFormSerializer,
                                  SellPropertyFormSerializer,)

from services.choices import FINISHING_CHOICES

#
class OrientationFormView(APIView):
    def post(self, request, format=None):
        serializer = OrientationFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)

#

    
class ServicemodelView(ListAPIView):
    queryset = Servicemodel.objects.all()
    serializer_class = ServicemodelSerializer

    def get_queryset(self):
        locale = self.request.GET.get('locale')
        if locale is None:
            raise APIException("Language parameter 'locale' is required.")
        
        languages = locale.lower().split(',')
        queryset = self.queryset.filter(locale__language_code__in=languages)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})



#        
class PostSaleServiceFormView(APIView):
    def post(self, request, format=None):
        serializer = PostSaleServiceFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)

#
class ConsultingFormView(APIView):
    def post(self, request, format=None):
        serializer = ConsultingFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
        
#
class OnlineVisitFormView(APIView):
    def post(self, request, format=None):
        serializer = OnlineVisitFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
        

#
class SellPropertyFormView(APIView):
    def post(self, request, format=None):
        serializer = SellPropertyFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)


#
class ApartmentExchangeFormView(APIView):
    def post(self, request, format=None):
        serializer = ApartmentExchangeFormSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)



#
class FinishingChoiceListView(APIView):
    def get(self, request):
        choices_data = [{'choice': choice[0]} for choice in FINISHING_CHOICES]
        serializer = FinishingChoiceSerializer(choices_data, many=True)
        return Response(serializer.data)