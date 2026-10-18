from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from quiz_app.models import QuizforQuizly
from .serializers import QuizDetailSerializer, QuizListSerializer

class QuizListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizListSerializer

    def get_queryset(self):
        return QuizforQuizly.objects.filter(
            user=self.request.user,
        ).order_by("-created_at")


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizDetailSerializer

    def get_queryset(self):
        return QuizforQuizly.objects.filter(
            user=self.request.user,
        ).prefetch_related("questions")
