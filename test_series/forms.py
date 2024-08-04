from django import forms
from .models import ProctoringEvent

class StartProctoringSessionForm(forms.Form):
    exam_id = forms.IntegerField()
    duration = forms.DurationField(required=False, help_text="Duration of the session (e.g., '1:30:00' for 1 hour 30 minutes)")

class EndProctoringSessionForm(forms.Form):
    session_id = forms.IntegerField()

class RecordProctoringEventForm(forms.ModelForm):
    session_id = forms.IntegerField()

    class Meta:
        model = ProctoringEvent
        fields = ['event_type', 'details', 'session_id']

# class UserResponseForm(forms.ModelForm):
#     class Meta:
#         model = UserResponse
#         fields = ['response']  

class SubmitAnswerForm(forms.Form):
    session_id = forms.IntegerField()
    question_no = forms.IntegerField()
    selected_option = forms.CharField(max_length=255)        


