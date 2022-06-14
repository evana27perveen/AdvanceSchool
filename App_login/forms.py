from django import forms
from .models import *
from django.contrib.auth import forms as auth_form
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _



class TeacherUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class TeacherForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = TeacherModel
        exclude = ['user', 'joining_date', ]


class StudentUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = StudentModel
        exclude = ['user', 'joining_date', ]


class ParentUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ParentForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = ParentModel
        exclude = ['user', ]


class StaffUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class StaffForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = NonTeachingStaffModel
        exclude = ['user', 'joining_date', ]


class LibrarianUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LibrarianForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = LibrarianModel
        exclude = ['user', 'joining_date', ]


class AccountantUserForm(auth_form.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class AccountantForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': _('Phone')}),
                                    label=_("Phone number"), required=True)

    class Meta:
        model = AccountantModel
        exclude = ['user', 'joining_date', ]
