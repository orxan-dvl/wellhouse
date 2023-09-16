from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from wagtail.models import Locale

from employee.models import Languages, Profession, Employee
from employee.serializers import LanguagesSerializer, ProfessionSerializer, EmployeeSerializer


#
class LanguagesListView(ListAPIView):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer

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
class LanguageDetailView(RetrieveAPIView):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")

        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Languages.objects.get(slug2=slug2, locale_id=locale.id)
        except Languages.DoesNotExist:
            raise NotFound("Languages object not found.")
        
#-------------------------------------------------------

class ProfessionListView(ListAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

    def get_queryset(self):
        locale = self.request.GET.get('locale')
        if not locale:
            raise APIException("Language parameter 'locale' is required.")
        return Profession.objects.filter(locale__language_code=locale)


#
class ProfessionDetailView(RetrieveAPIView):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")
        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Profession.objects.get(slug2=slug2, locale_id=locale.id)
        except Profession.DoesNotExist:
            raise NotFound("Profession object not found.")

#------------------------------------

#
#
class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        locale = self.request.GET.get('locale')
        if not locale:
            raise APIException("Language parameter 'locale' is required.")
        return Employee.objects.filter(locale__language_code=locale)


#
class EmployeeDetailView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'slug2'

    def get_object(self):
        locale_code = self.request.GET.get('locale')
        if not locale_code:
            raise APIException("Language parameter 'locale' is required.")
        locale = Locale.objects.filter(language_code=locale_code).last()
        slug2 = self.kwargs['slug2']

        try:
            return Employee.objects.get(slug2=slug2, locale_id=locale.id)
        except Employee.DoesNotExist:
            raise NotFound("Employee object not found.")
