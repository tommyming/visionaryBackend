from quiz.models import LearningQuiz, LearningOption, LearningSummary
from rest_framework import serializers


class LearningOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningOption
        fields = "__all__"


class LearningQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningQuiz
        fields = "__all__"


class LearningSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningSummary
        fields = "__all__"
