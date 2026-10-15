from rest_framework import serializers
from quiz_app.models import QuestionforQuizly, QuizforQuizly

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
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
        current_options = getattr(self.instance, "question_options", [])
        current_answer = getattr(self.instance, "answer", None)
        options = attrs.get("question_options", current_options)
        answer = attrs.get("answer", current_answer)
        if answer not in options:
            message = "Answer must be one of the question options."
            raise serializers.ValidationError({"answer": message})
        return attrs


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
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
    class Meta:
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
