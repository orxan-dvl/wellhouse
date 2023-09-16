from rest_framework.serializers import ModelSerializer, SerializerMethodField

from employee.models import Languages, Profession, Employee

#
class LanguagesSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = Languages
        fields = ['id', 'language_name', 'slug2', 'locale', 'created_at' ]

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation

#
class ProfessionSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = Profession
        fields = ['id', 'profession', 'slug2', 'locale', 'created_at' ]

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation

class EmployeeSerializer(ModelSerializer):
    locale = SerializerMethodField()
    profession = ProfessionSerializer()
    languages_spoken = LanguagesSerializer(many=True)

    class Meta:
        model = Employee
        fields = ('id', 'slug2', 'locale', 'fullname', 'profession', 'phone_number', 
                  'email', 'image', 'languages_spoken')


    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation
