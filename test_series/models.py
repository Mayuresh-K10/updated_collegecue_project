from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Exam(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()

class ProctoringSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')])
    duration = models.DurationField(default=timezone.timedelta(hours=1))

class ProctoringEvent(models.Model):
    session = models.ForeignKey(ProctoringSession, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)
    EVENT_TYPES = [
      ('face_not_detected', 'Face Not Detected'),
      ('multiple_people_detected', 'Multiple People Detected'),
      ('unauthorized_material', 'Unauthorized Material Detected'),
      ('screen_change_detected', 'Screen Change Detected'),
      ]

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_no = models.IntegerField(unique=True)
    question_name = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    time_limit = models.DurationField(default=timedelta(seconds=30))
    time_limit = models.DurationField(default=timedelta(seconds=30))
    correct_option = models.CharField(max_length=255,default='option1')

class UserResponse(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    session = models.ForeignKey(ProctoringSession, on_delete=models.CASCADE)

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
