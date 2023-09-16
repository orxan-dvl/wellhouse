from rest_framework.views import APIView
from rest_framework.response import Response

from feedback.serializers import FeedbackSerializer, GenderChoiceSerializer
from feedback.choices import GENDER_CHOICES

#
class FeedbackView(APIView):
    def post(self, request, format=None):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
        
#
class GenderChoiceListView(APIView):
    def get(self, request):
        choices_data = [{'choice': choice[0]} for choice in GENDER_CHOICES]
        serializer = GenderChoiceSerializer(choices_data, many=True)
        return Response(serializer.data)