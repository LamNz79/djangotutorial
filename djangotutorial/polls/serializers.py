from rest_framework import serializers

from polls.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source="choice_text")
    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Choice
        fields = ["id", "text", "vote_count"]


class ChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["choice_text"]


class QuestionSerializers(serializers.ModelSerializer):
    question = serializers.CharField(source="question_text")
    created_date = serializers.DateTimeField(source="pub_date")
    choices = ChoiceSerializer(many=True, read_only=True, source="choice_set")
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question", "created_date", "choices", "total_votes"]


class QuestionCreateSerializer(serializers.ModelSerializer):
    choices = ChoiceCreateSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ["question_text", "pub_date", "choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop("choices", [])
        question = Question.objects.create(**validated_data)
        if choices_data:
            Choice.objects.bulk_create([
                Choice(question=question, **choice)
                for choice in choices_data
            ])
        return question
