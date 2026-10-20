"""Validate generated quiz data and persist it atomically."""
from django.db import transaction
from rest_framework import serializers
from quiz_app.models import QuestionforQuizly, QuizforQuizly

class GeneratedQuestionSerializer(serializers.Serializer):
    """Validate a question returned by the generation service."""
    question_title = serializers.CharField(max_length=400)
    question_options = serializers.ListField(
        child=serializers.CharField(max_length=400),
        min_length=4,
        max_length=4,
    )
    answer = serializers.CharField(max_length=400)

    def validate(self, attrs):
        """Require four distinct options containing the answer."""
        options = attrs["question_options"]
        if len(set(options)) != 4:
            raise serializers.ValidationError("Question options must be distinct.")
        if attrs["answer"] not in options:
            raise serializers.ValidationError("Answer must be one of the options.")
        return attrs


class GeneratedQuizSerializer(serializers.Serializer):
    """Validate a complete quiz returned by the generation service."""

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=150)
    questions = GeneratedQuestionSerializer(many=True)

    def validate_questions(self, questions):
        """Require every generated quiz to contain ten questions."""
        if len(questions) != 10:
            raise serializers.ValidationError("A quiz must contain 10 questions.")
        return questions


def build_question(quiz, question_data):
    """Build an unsaved question linked to the supplied quiz."""
    return QuestionforQuizly(quizz=quiz, **question_data)


@transaction.atomic
def save_generated_quiz(quiz_data, user, video_url):
    """Validate and atomically save a generated quiz and its questions."""
    serializer = GeneratedQuizSerializer(data=quiz_data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data.copy()
    questions = validated_data.pop("questions")
    quiz = QuizforQuizly.objects.create(
        user=user, video_url=video_url, **validated_data
    )
    question_objects = [build_question(quiz, data) for data in questions]
    QuestionforQuizly.objects.bulk_create(question_objects)
    return quiz
