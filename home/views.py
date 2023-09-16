from rest_framework.views import APIView
from rest_framework.response import Response

from home.modelserializers import (HelpForPropertyChoiceFormSerializer, AskQuestionFormSerializer, 
                                   AskCallFormSerializer)

#
class HelpForPropertyView(APIView):
    def post(self, request, format=None):
        serializer = HelpForPropertyChoiceFormSerializer(data=request.data)
        if serializer.is_valid():
            help_form = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
        
#
class AskQuestionFormView(APIView):
    def post(self, request, format=None):
        serializer = AskQuestionFormSerializer(data=request.data)
        if serializer.is_valid():
            ask_question_form = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)

#
class AskCallFormView(APIView):
    def post(self, request, format=None):
        serializer = AskCallFormSerializer(data=request.data)
        if serializer.is_valid():
            ask_question_form = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        else:
            return Response(serializer.errors, status=400)
