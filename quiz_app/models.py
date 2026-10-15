from django.db import models
from django.conf import settings

class QuizforQuizly(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=True,null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes',
    )


    def __str__(self):
        return f"Quizz {self.id}, {self.title}  by {self.user.username}"
    

class QuestionforQuizly(models.Model):    
    quizz = models.ForeignKey(QuizforQuizly, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=400)
    question_options = models.JSONField()
    answer=models.CharField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Quizz  {self.quizz.title} - {self.question_title}"
