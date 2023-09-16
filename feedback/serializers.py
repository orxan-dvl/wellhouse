from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer, CharField

from employee.models import Employee
from feedback.forms import Feedback
from feedback.choices import GENDER_CHOICES



#
class FeedbackIndexSerializer(serializers.Serializer):
    def to_representation(self, value):
        data_list = []
        for i in value:
            data = {
                'name': i.name,
                'surname': i.surname,
                'country': i.country,
                'message': i.message,
                'datetime': i.created_at,
                'employee': {
                    'fullname': i.employee_for_feedback.fullname if i.employee_for_feedback else None,
                }
            }
            data_list.append(data)
        return data_list
    

#Serializer for Feedback model
class FeedbackSerializer(ModelSerializer):
    employee_for_feedback = PrimaryKeyRelatedField(queryset=Employee.objects.all())


    class Meta:
        model = Feedback
        fields = ('id', 'name', 'surname', 'country', 'gender', 'email', 'message', 
                  'employee_for_feedback', 'created_at', 'has_been_read')

    gender = serializers.ChoiceField(choices=GENDER_CHOICES)


#
class GenderChoiceSerializer(Serializer):
    choice = CharField()