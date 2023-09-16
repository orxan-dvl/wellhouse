from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import APIException, NotFound

from wagtail.models import Locale

from advertisement.models import Type, City, Region, Category, Room, Tags
from advertisement.forms import PropertyRequestTypes
from advertisement.modelserializers import (TypeSerializer, CitySerializer, RegionSerializer, 
                                            CategorySerializer, PropertyRequestTypesSerializer, 
                                            PropertyDetailFormSerializer, RoomSerializer, 
                                            PropertyDetailOnlineVisitFormSerializer, TagSerializer)


@api_view(["GET"])
def region_filter_by_locale(request):
    lang_param = request.GET.get('locale')
    queryset = Region.objects.filter(locale__language_code=lang_param)
    serializer = RegionSerializer(queryset, many=True)
    return JsonResponse({"data": serializer.data})


@api_view(["GET"])
def region_filter_by_city(request, city_slug2):
    city = City.objects.filter(slug2=city_slug2).first()
    lang_param = request.GET.get('locale')

    regions = Region.objects.filter(city_rel=city)

    if lang_param and lang_param.lower() != 'all':
        languages = lang_param.lower().split(',')
        regions = regions.filter(city_rel__locale__language_code__in=languages)

    serializer = RegionSerializer(regions, many=True)
    return JsonResponse({"data": serializer.data})



    
#----------------------------Type views-------------------------------------

#    
class TypeListView(ListAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

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
class TypeDetailView(RetrieveAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Type.objects.get(slug2=slug2, locale_id=locale.id)
        except Type.DoesNotExist:
            raise NotFound("Type object not found.")

#----------------------------------------Room views-------------------------------------

#    
class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = TypeSerializer

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
class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Room.objects.get(slug2=slug2, locale_id=locale.id)
        except Room.DoesNotExist:
            raise NotFound("Type object not found.")



#-----------------------------------Category views--------------------------
#
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Category.objects.get(slug2=slug2, locale_id=locale.id)
        except Category.DoesNotExist:
            raise NotFound("Category object not found.")

#-----------------------------------Tags views--------------------------
#
class TagsListView(ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

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
class TagsDetailView(RetrieveAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Tags.objects.get(slug2=slug2, locale_id=locale.id)
        except Tags.DoesNotExist:
            raise NotFound("Category object not found.")



#-----------------------------City views------------------------------------------------

#
class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

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
class CityDetailView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug2'

    def get_queryset(self):
        locale = self.request.GET.get('locale')
        if locale is None:
            raise APIException("Language parameter 'locale' is required.")

        languages = locale.lower().split(',')
        queryset = self.queryset.filter(locale__language_code__in=languages)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except City.DoesNotExist:
            raise NotFound("City object not found.")

        serializer = self.get_serializer(instance)

        locale = self.request.GET.get('locale')
        if locale:
            languages = locale.lower().split(',')
            regions = Region.objects.filter(city_rel=instance, locale__language_code__in=languages)
        else:
            regions = Region.objects.filter(city_rel=instance)

        region_serializer = RegionSerializer(regions, many=True)

        response_data = {
            "city": serializer.data,
            "regions": region_serializer.data
        }

        return Response(response_data)




#----------------------------------Region views-------------------------------------

#
class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

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
class RegionDetailView(RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Region.objects.get(slug2=slug2, locale_id=locale.id)

        except Region.DoesNotExist:
            raise NotFound("Type object not found.")



#-----------------------------PropertyDetailForm views---------------------------------


#PropertyRequestTypes view
class PropertyRequestTypesView(ListAPIView):
    queryset = PropertyRequestTypes.objects.all()
    serializer_class = PropertyRequestTypesSerializer

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
    


#PropertyDetailForm view
class PropertyDetailFormView(APIView):
    def post(self, request, format=None):
        serializer = PropertyDetailFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
        
#PropertyDetailOnlineVisitForm and PropertyDetailOrientationForm
class PropertyDetailOnlineVisitFormView(APIView):
    def post(self, request, format=None):
        serializer = PropertyDetailOnlineVisitFormSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)

