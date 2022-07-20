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
        exclude = ['provider', 'created', 'status', ]


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


class RoutineModelForm(forms.ModelForm):
    class Meta:
        model = RoutineModel
        exclude = ['user', 'created', 'status', ]


class NoticeModelForm(forms.ModelForm):
    class Meta:
        model = NoticeModel
        exclude = ['user', 'created', 'status', ]


class StudentFeesModelForm(forms.ModelForm):
    class Meta:
        model = StudentFeesModel
        fields = ['semester_fee', ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['title', ]


class AddBookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = "__all__"


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowModel
        exclude = ['quantity', 'date', 'status', 'user']


class BookEditForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ['title', 'cover', 'author', 'description', 'available', 'location']


class AddNewSelf(forms.ModelForm):
    class Meta:
        model = BookLocationModel
        fields = ['self_no', 'row_no']
