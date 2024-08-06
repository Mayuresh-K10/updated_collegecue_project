# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST, require_GET
# from .models import ProctoringEvent, ProctoringSession, Exam, Question, UserResponse, UserScore
# from .forms import StartProctoringSessionForm, EndProctoringSessionForm, RecordProctoringEventForm, SubmitAnswerForm
# from django.contrib.auth import authenticate, login as auth_login
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.models import User
# from rest_framework.views import APIView
#
# @csrf_exempt
# @require_POST
# def custom_login(request):
#     try:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#          auth_login(request, user)
#          return JsonResponse({'message': 'Login successful'})
#         else:
#          return JsonResponse({'error': 'Invalid credentials'}, status=400)
#     except Exception as e:
#      return JsonResponse({'error': 'An error occurred during login'}, status=500)

# @login_required
# @require_POST
# @csrf_exempt
# def start_proctoring_session(request):
# try:
#     form = StartProctoringSessionForm(request.POST)
#     if form.is_valid():
#         exam_id = form.cleaned_data['exam_id']
#         exam = get_object_or_404(Exam, id=exam_id)
#         session = ProctoringSession.objects.create(
#             user=request.user,
#             exam=exam,
#             start_time=timezone.now(),
#             status='ongoing'
#         )
#         user_email= User.objects.get(username=request.user).email
#         try:
#            send_mail("Proctoring Event Notification","Session started",settings.EMAIL_HOST_USER,[user_email])
#         except:
#            print("Email not send")
#         return JsonResponse({'session_id': session.id})
#     else:
#         return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)
# except Exception as e:

# @login_required
# @require_POST
# @csrf_exempt
# def end_proctoring_session(request):
#     form = EndProctoringSessionForm(request.POST)
#     if form.is_valid():
#         session_id = form.cleaned_data['session_id']
#         session = get_object_or_404(ProctoringSession, id=session_id)
#         session.end_time = timezone.now()
#         session.status = 'completed'
#         session.save()

#         user_email= User.objects.get(username=request.user).email
#         try:
#          send_mail("Proctoring Event Notification","Session ended",settings.EMAIL_HOST_USER,[user_email])
#         except:
#          print("Email not send")
#         return JsonResponse({'status': 'completed'})
#     else:
#         return JsonResponse({'error': 'Invalid data'}, status=400)


# @login_required
# @require_POST
# @csrf_exempt
# def record_proctoring_event(request):
#     form = RecordProctoringEventForm(request.POST)
#     if form.is_valid():
#         event = form.save(commit=False)
#         session_id = form.cleaned_data['session_id']
#         event.session = get_object_or_404(ProctoringSession, id=session_id)
#         event.save()
#         user_email= User.objects.get(username=request.user).email
#         try:
#          send_mail("Proctoring Event Notification","Session Recorded",settings.EMAIL_HOST_USER,[user_email])
#         except:
#          print("Email not send")

#         return JsonResponse({'status': 'event recorded'})
#     else:
#         return JsonResponse({'error': 'Invalid data'}, status=400)

# def count_questions(request):
#     question_count = Question.objects.count()
#     return JsonResponse({'question_count': question_count})

# class EventTypesAPIView(APIView):
#     def get(self, request, fmt=None):
#         event_types = dict(ProctoringEvent.EVENT_TYPES)
#         return JsonResponse({'event_types': event_types})

# @login_required
# @require_POST
# @csrf_exempt
# def submit_answer(request):
#     form = SubmitAnswerForm(request.POST)
#     if form.is_valid():
#         session_id = form.cleaned_data['session_id']
#         question_no = form.cleaned_data['question_no']
#         selected_option = form.cleaned_data['selected_option']

#         session = get_object_or_404(ProctoringSession, id=session_id)
#         question = get_object_or_404(Question, question_no=question_no)

#         user_response, created = UserResponse.objects.get_or_create(
#             user=request.user,
#             question=question,
#             session=session,
#             defaults={'start_time': timezone.now()}
#         )

#         if not created:
#             time_taken = timezone.now() - user_response.start_time
#             if time_taken.total_seconds() > question.time_limit.total_seconds():
#                 return JsonResponse({'error': 'Time limit exceeded'}, status=400)

#         is_correct = (selected_option == question.correct_option)
#         user_response.end_time = timezone.now()
#         user_response.response = selected_option
#         user_response.save()

#         if is_correct:
#             user_score, created = UserScore.objects.get_or_create(user=session.user, exam=session.exam)
#             user_score.score += 1
#             user_score.save()

#         response_message = "Correct answer!" if is_correct else f"Incorrect answer. The correct option was: {question.correct_option}"
#         return JsonResponse({'message': response_message})
#     else:
#         return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)

# @csrf_exempt
# @login_required
# def get_session_status(request, session_id):
#     session = get_object_or_404(ProctoringSession, id=session_id)
#     data = {
#         'status': session.status,
#         'start_time': session.start_time,
#         'end_time': session.end_time,
#         'duration': session.duration.total_seconds()
#     }
#     return JsonResponse(data)

# @login_required
# @csrf_exempt
# def get_question_details(request, question_no):
#     question = get_object_or_404(Question, question_no=question_no)
#     data = {
#         'question_no': question.question_no,
#         'question_name': question.question_name,
#         'options': [question.option1, question.option2, question.option3, question.option4],
#         'time_limit': question.time_limit.total_seconds()
#     }
#     return JsonResponse(data)

# @login_required
# @csrf_exempt
# @require_GET
# def get_user_score(request, exam_id):
#     user = request.user
#     exam = get_object_or_404(Exam, id=exam_id)
#     user_score = get_object_or_404(UserScore, user=user, exam=exam)

#     response_data = {
#         'user': user.username,
#         'exam': exam.name,
#         'score': user_score.score
#     }
#     return JsonResponse(response_data)



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import ProctoringEvent, ProctoringSession, Exam, Question, UserResponse, UserScore
from .forms import StartProctoringSessionForm, EndProctoringSessionForm, RecordProctoringEventForm, SubmitAnswerForm
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView

@csrf_exempt
@require_POST
def custom_login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during login', 'details': str(e)}, status=500)

@login_required
@require_POST
@csrf_exempt
def start_proctoring_session(request):
    try:
        form = StartProctoringSessionForm(request.POST)
        if form.is_valid():
            exam_id = form.cleaned_data['exam_id']
            exam = get_object_or_404(Exam, id=exam_id)
            
            if ProctoringSession.objects.filter(user=request.user, exam=exam).exists():
                return JsonResponse({'error': 'Proctoring session for this exam already exists'}, status=400)
            
            session = ProctoringSession.objects.create(
                user=request.user,
                exam=exam,
                start_time=timezone.now(),
                status='ongoing'
            )
            
            user_email = request.user.email
            try:
                send_mail(
                    "Proctoring Event Notification",
                    "Session started",
                    settings.EMAIL_HOST_USER,
                    [user_email]
                )
            except Exception as email_error:
                return JsonResponse({'error': 'Failed to send email notification', 'details': str(email_error)}, status=500)
            
            return JsonResponse({'session_id': session.id}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while starting the session', 'details': str(e)}, status=500)

@login_required
@require_POST
@csrf_exempt
def end_proctoring_session(request):
    try:
        form = EndProctoringSessionForm(request.POST)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            session = get_object_or_404(ProctoringSession, id=session_id)
            session.end_time = timezone.now()
            session.status = 'completed'
            session.save()
            user_email = request.user.email
            try:
                send_mail("Proctoring Event Notification", "Session ended", settings.EMAIL_HOST_USER, [user_email])
            
            except Exception as email_error:
                return JsonResponse({'error': f"Failed to send email to {user_email}: {email_error}"}, status=500)
            
            return JsonResponse({'status': 'completed'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while ending the session', 'details': str(e)}, status=500)

@login_required
@require_POST
@csrf_exempt
def record_proctoring_event(request):
    try:
        form = RecordProctoringEventForm(request.POST)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            session = get_object_or_404(ProctoringSession, id=session_id)

            if ProctoringEvent.objects.filter(session=session).exists():
                return JsonResponse({'error': 'Event for this session already recorded'}, status=400)
            
            event = form.save(commit=False)
            event.session = session
            event.save()
            
            user_email = request.user.email
            try:
                send_mail(
                    "Proctoring Event Notification",
                    "Event recorded",
                    settings.EMAIL_HOST_USER,
                    [user_email]
                )
            except Exception as email_error:
                return JsonResponse({'status': 'event recorded', 'email_error': str(email_error)}, status=200)
            
            return JsonResponse({'status': 'event recorded'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while recording the event', 'details': str(e)}, status=500)

@login_required
@require_GET
def get_question_details(request, question_no):
    try:
        question = get_object_or_404(Question, question_no=question_no)
        response_data = {
            'question_no': question.question_no,
            'question_name': question.question_name,
            'options': [question.option1, question.option2, question.option3, question.option4],
            'time_limit': question.time_limit.total_seconds()
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching question details','details':str(e)}, status=500)


@login_required
@csrf_exempt
@require_POST
def submit_answer(request):
    try:
        form = SubmitAnswerForm(request.POST)
        if form.is_valid():
            session_id = form.cleaned_data['session_id']
            question_no = form.cleaned_data['question_no']
            selected_option = form.cleaned_data['selected_option']

            
            session = get_object_or_404(ProctoringSession, id=session_id)
            question = get_object_or_404(Question, question_no=question_no)

            
            user_response, created = UserResponse.objects.get_or_create(
                user=request.user,
                question=question,
                session=session,
                defaults={'start_time': timezone.now()}
            )

            if not created:
                time_taken = timezone.now() - user_response.start_time
                if time_taken.total_seconds() > question.time_limit.total_seconds():
                    return JsonResponse({'error': 'Time limit exceeded'}, status=400)

           
            user_response.end_time = timezone.now()
            user_response.response = selected_option
            user_response.save()

            is_correct = (selected_option == question.correct_option)

            if is_correct:
                user_score, created = UserScore.objects.get_or_create(user=session.user, exam=session.exam)
                user_score.score += 1
                user_score.save()

            response_message = "Correct answer!" if is_correct else f"Incorrect answer. The correct option was: {question.correct_option}"

            return JsonResponse({'message': response_message}, status=200)

        else:
            return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while submitting the answer','details':str(e)}, status=500)


@login_required
@require_GET
def get_session_status(request, session_id):
    try:
        session = get_object_or_404(ProctoringSession, id=session_id)
        data = {
        'status': session.status,
        'start_time': session.start_time,
        'end_time': session.end_time,
        'duration': session.duration.total_seconds()
    }
        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching session status','details':str(e)}, status=500)


@login_required
@require_GET
def get_user_score(request, exam_id):
    try:
        user = request.user
        exam = get_object_or_404(Exam, id=exam_id)
        user_score = get_object_or_404(UserScore, user=user, exam=exam)
        
        response_data = {
            'user': user.username,
            'exam': exam.name,
            'score': user_score.score
        }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching user score','details':str(e)}, status=500)

def count_questions(request, exam_id):
    try:
        exam = Exam.objects.filter(id=exam_id).first()
        if not exam:
            return JsonResponse({'error': 'Exam ID not found'}, status=404)
        
        question_count = Question.objects.filter(exam_id=exam_id).count()
        
        if question_count == 0:
            return JsonResponse({'error': 'No Questions found for this Exam', 'exam_name': exam.name}, status=404)
        else:
            return JsonResponse({'question_count': question_count, 'exam_name': exam.name}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': f'An error occurred while counting questions: {str(e)}'}, status=500)

class EventTypesAPIView(APIView):
    def get(self, request, fmt=None):
        try:
            event_types = dict(ProctoringEvent.EVENT_TYPES)
            return JsonResponse({'event_types': event_types}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while fetching event types','details':str(e)}, status=500)
            