from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from usefull.modelserializers import SubscriberSerializer



class SubscribeAPIView(APIView):
    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            form = serializer.save()
            return Response({'message': 'Form submitted successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
