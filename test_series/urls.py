from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('proctoring/start/', views.start_proctoring_session, name='start_proctoring_session'),
    path('proctoring/end/', views.end_proctoring_session, name='end_proctoring_session'),
    path('proctoring/event/', views.record_proctoring_event, name='record_proctoring_event'),
    path('count-questions/<int:exam_id>/', views.count_questions, name='count_questions'),
    path('event-types/', views.EventTypesAPIView.as_view(), name='event-types'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('session-status/<int:session_id>/', views.get_session_status, name='get_session_status'),
    path('question/<int:question_no>/', views.get_question_details, name='get_question_details'),
    path('user-score/<int:exam_id>/', views.get_user_score, name='get_user_score'),
]