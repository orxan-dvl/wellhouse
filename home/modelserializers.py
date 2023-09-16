from rest_framework.serializers import ModelSerializer

from home.forms import (HelpForPropertyChoiceForm, AskQuestionForm, AskCallForm, )


#
class HelpForPropertyChoiceFormSerializer(ModelSerializer):

    class Meta:
        model = HelpForPropertyChoiceForm
        fields = '__all__'

#
class AskQuestionFormSerializer(ModelSerializer):
    class Meta:
        model = AskQuestionForm
        fields = '__all__'

#
class AskCallFormSerializer(ModelSerializer):
    class Meta:
        model = AskCallForm
        fields = '__all__'