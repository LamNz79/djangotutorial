from rest_framework import serializers

from polls.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source="choice_text")

    class Meta:
        model = Choice
        fields = ["id", "text", "votes"]


class QuestionSerializers(serializers.ModelSerializer):
    question = serializers.CharField(source="question_text")
    created_date = serializers.DateTimeField(source="pub_date")
    choices = ChoiceSerializer(many=True, read_only=True, source="choice_set")
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question", "created_date", "choices","total_votes"]
