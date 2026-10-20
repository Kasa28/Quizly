"""Authenticated API views for generating and managing quizzes."""
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from quiz_app.models import QuizforQuizly
from quiz_app.services.quiz_generation import generate_quiz_from_youtube
from quiz_app.services.quiz_storage import save_generated_quiz
from .serializers import (QuizDetailSerializer, QuizGenerationSerializer, QuizListSerializer)

class QuizListView(ListAPIView):
    """List a user's quizzes and generate new quizzes."""

    permission_classes = [IsAuthenticated]
    serializer_class = QuizListSerializer

    def get_queryset(self):
        """Return only quizzes owned by the authenticated user."""
        return QuizforQuizly.objects.filter(
            user=self.request.user,
        ).order_by("-created_at")

    def post(self, request):
        """Generate, validate, save, and return a YouTube quiz."""
        serializer = QuizGenerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video_url = serializer.validated_data["url"]
        quiz_data = generate_quiz_from_youtube(video_url)
        quiz = save_generated_quiz(quiz_data, request.user, video_url)
        return Response(
            QuizDetailSerializer(quiz).data,
            status=status.HTTP_201_CREATED,
        )


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete one quiz owned by the user."""

    permission_classes = [IsAuthenticated]
    serializer_class = QuizDetailSerializer

    def get_queryset(self):
        """Return owned quizzes with their questions prefetched."""
        return QuizforQuizly.objects.filter(
            user=self.request.user,
        ).prefetch_related("questions")
