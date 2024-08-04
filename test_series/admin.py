from django.contrib import admin
from .models import Exam, ProctoringSession, ProctoringEvent, Question, UserResponse, UserScore

admin.site.register(Exam)
admin.site.register(ProctoringSession)
admin.site.register(ProctoringEvent)
admin.site.register(Question)
admin.site.register(UserResponse)
admin.site.register(UserScore)