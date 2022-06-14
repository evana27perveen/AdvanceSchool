from django import forms
from django.forms import Textarea

from App_main.models import *


class AssignmentForm(forms.ModelForm):
    deadline = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = AssignmentModel
        exclude = ['test_provider', 'created', 'status', ]


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmissionModel
        fields = ['submission_file', ]


class AttendanceModelForm(forms.ModelForm):
    class Meta:
        model = AttendanceModel
        exclude = ['teacher', 'student', 'status', 'date']


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        exclude = ['test_provider', 'created', 'status', ]


class TestSubmissionForm(forms.ModelForm):
    class Meta:
        model = TestSubmissionModel
        fields = ['submission_file', ]
