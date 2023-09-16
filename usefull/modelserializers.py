from usefull.models import SubscriberForm
from rest_framework.serializers import ModelSerializer

#
class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = SubscriberForm
        fields = ('email',)