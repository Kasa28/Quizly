"""Django admin registrations for quizzes and questions."""

from django.contrib import admin
from .models import QuizforQuizly, QuestionforQuizly

admin.site.register(QuizforQuizly)
admin.site.register(QuestionforQuizly)
