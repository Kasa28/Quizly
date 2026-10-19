from django.urls import path
from .views import QuizDetailView, QuizGenerationView, QuizListView

urlpatterns = [
    path("quizzes/", QuizListView.as_view(), name="quiz-list"),
    path("quizzes/generate/", QuizGenerationView.as_view(), name="quiz-generate"),
    path("quizzes/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
]
