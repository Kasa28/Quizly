"""Serializers for quiz generation and API representations."""

from rest_framework import serializers
from quiz_app.models import QuestionforQuizly, QuizforQuizly


class QuizGenerationSerializer(serializers.Serializer):
    """Validate the URL submitted for quiz generation."""

    url = serializers.URLField()

class QuestionSerializer(serializers.ModelSerializer):
    """Serialize stored quiz questions and validate their answers."""

    class Meta:
        """Configure fields exposed for a quiz question."""
        model = QuestionforQuizly
        fields = (
            "id",
            "question_title",
            "question_options",
            "answer",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        """Ensure the correct answer is included in the options."""
        current_options = getattr(self.instance, "question_options", [])
        current_answer = getattr(self.instance, "answer", None)
        options = attrs.get("question_options", current_options)
        answer = attrs.get("answer", current_answer)
        if answer not in options:
            message = "Answer must be one of the question options."
            raise serializers.ValidationError({"answer": message})
        return attrs


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serialize a quiz together with all nested questions."""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        """Configure fields exposed for quiz details."""
        model = QuizforQuizly
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        )
        read_only_fields = ("id", "created_at", "updated_at", "video_url")


class QuizListSerializer(serializers.ModelSerializer):
    """Serialize compact quiz data for the user's quiz list."""

    class Meta:
        """Configure fields exposed in the quiz list."""
        model = QuizforQuizly
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
        )
        read_only_fields = ("id", "created_at", "updated_at", "video_url")
