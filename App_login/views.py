from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import *
from .forms import *


# Create your views here.


def teacher_signup(request):
    form1 = TeacherUserForm()
    form2 = TeacherForm()
    if request.method == 'POST':
        form1 = TeacherUserForm(data=request.POST)
        form2 = TeacherForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            teacher_grp = Group.objects.get_or_create(name='TEACHER')
            teacher_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/teacher_signup.html', context={'form1': form1, 'form2': form2})


def student_signup(request):
    form1 = StudentUserForm()
    form2 = StudentForm()
    if request.method == 'POST':
        form1 = StudentUserForm(data=request.POST)
        form2 = StudentForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            student_grp = Group.objects.get_or_create(name='STUDENT')
            student_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/student_signup.html', context={'form1': form1, 'form2': form2})


def parent_signup(request):
    form1 = ParentUserForm()
    form2 = ParentForm()
    if request.method == 'POST':
        form1 = ParentUserForm(data=request.POST)
        form2 = ParentForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            parent_grp = Group.objects.get_or_create(name='PARENT')
            parent_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/parent_signup.html', context={'form1': form1, 'form2': form2})


def staff_signup(request):
    form1 = StaffUserForm()
    form2 = StaffForm()
    if request.method == 'POST':
        form1 = StaffUserForm(data=request.POST)
        form2 = StaffForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            staff_grp = Group.objects.get_or_create(name='STAFF')
            staff_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/staff_signup.html', context={'form1': form1, 'form2': form2})


def librarian_signup(request):
    form1 = LibrarianUserForm()
    form2 = LibrarianForm()
    if request.method == 'POST':
        form1 = LibrarianUserForm(data=request.POST)
        form2 = LibrarianForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            librarian_grp = Group.objects.get_or_create(name='LIBRARIAN')
            librarian_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/librarian_signup.html', context={'form1': form1, 'form2': form2})


def accountant_signup(request):
    form1 = AccountantUserForm()
    form2 = AccountantForm()
    if request.method == 'POST':
        form1 = AccountantUserForm(data=request.POST)
        form2 = AccountantForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            my_form1 = form1.save()
            my_form2 = form2.save(commit=False)
            my_form2.user = my_form1
            my_form2.save()
            accountant_grp = Group.objects.get_or_create(name='ACCOUNTANT')
            accountant_grp[0].user_set.add(my_form1)
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    return render(request, 'App_login/accountant_signup.html', context={'form1': form1, 'form2': form2})


def login_system(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.groups.filter(name__in=['ADMIN']).exists():
                    return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
                elif request.user.groups.filter(name__in=['TEACHER']).exists():
                    return HttpResponseRedirect(reverse('App_main:teacher-dashboard'))
                elif request.user.groups.filter(name__in=['STUDENT']).exists():
                    return HttpResponseRedirect(reverse('App_main:student-dashboard'))
                elif request.user.groups.filter(name__in=['ACCOUNTANT']).exists():
                    return render(request, 'accountants/dashboard.html')
                elif request.user.groups.filter(name__in=['PARENT']).exists():
                    return render(request, 'parents/dashboard.html')
                elif request.user.groups.filter(name__in=['LIBRARIAN']).exists():
                    return render(request, 'librarians/dashboard.html')
                elif request.user.groups.filter(name__in=['STAFF']).exists():
                    return render(request, 'staff/dashboard.html')
                else:
                    return HttpResponseRedirect(reverse('App_login:login'))
    return render(request, 'App_login/login.html', context={'form': form})


def logout_system(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_login:login'))


