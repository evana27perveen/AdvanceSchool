from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from App_login.models import TeacherModel, StudentModel
from App_main.forms import AssignmentForm, AttendanceModelForm, TestModelForm, AssignmentSubmissionForm
from App_main.models import AssignmentSubmissionModel, AssignmentModel, AttendanceModel, TestSubmissionModel, TestModel


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def is_parent(user):
    return user.groups.filter(name='PARENT').exists()


def is_staff(user):
    return user.groups.filter(name='STAFF').exists()


def is_librarian(user):
    return user.groups.filter(name='LIBRARIAN').exists()


def is_accountant(user):
    return user.groups.filter(name='ACCOUNTANT').exists()


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    content = {
        'date': date,
    }
    return render(request, 'admins/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = TeacherModel.objects.get(user=request.user)
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))
    content = {
        'date': date,
        'profile': profile,
        'all_students': all_students.count(),
        'batch_list': batch_list,
    }
    return render(request, 'teachers/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def specific_dept_students(request, pk, dept):
    dept = dept.lower()
    students = StudentModel.objects.filter(batch=pk, department=dept)
    content = {
        'students': students,
    }
    return render(request, 'teachers/dept_students.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def student_disable(request, k):
    student = StudentModel.objects.get(id=k)
    student.status = False
    student.save()
    pk = student.batch
    dept = student.department
    return HttpResponseRedirect(reverse('App_main:specific-dept-students', kwargs={'pk': pk, 'dept': dept}))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def student_activate(request, k):
    student = StudentModel.objects.get(id=k)
    student.status = True
    student.save()
    pk = student.batch
    dept = student.department
    return HttpResponseRedirect(reverse('App_main:specific-dept-students', kwargs={'pk': pk, 'dept': dept}))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def new_assignment(request):
    form = AssignmentForm()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.provider = request.user
            assign.save()
            students = StudentModel.objects.filter(batch=assign.batch, department=assign.department,
                                                   section=assign.section)
            for student in students:
                a = AssignmentSubmissionModel(submitted_by=student, my_assignment=assign)
                a.save()
            return HttpResponseRedirect(reverse('App_main:assignment-submissions'))
    content = {
        'form': form,
    }
    return render(request, 'teachers/new_assignment.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def submitted_assignments(request):
    assignments = list(
        set(AssignmentModel.objects.filter(provider=request.user).values_list('Title').order_by('deadline')))
    submitted = AssignmentSubmissionModel.objects.filter(my_assignment__provider=request.user, status=True).order_by(
        '-my_assignment__deadline', '-created')

    content = {
        'assignments': assignments,
        'submissions': submitted,
    }
    return render(request, 'teachers/submitted_assignments.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def delete_assignments(request, pk):
    assignments = AssignmentModel.objects.filter(Title=pk)
    for i in assignments:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:teacher-dashboard'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def update_assignment_marks(request, pk):
    mark = request.POST.get('marks')
    assignment = AssignmentSubmissionModel.objects.get(id=pk)
    assignment.marks = mark
    assignment.save()
    return HttpResponseRedirect(reverse('App_main:assignment-submissions'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def take_attendance(request):
    form = AttendanceModelForm()
    if request.method == 'POST':
        form = AttendanceModelForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data.get('department')
            batch = form.cleaned_data.get('batch')
            semester = form.cleaned_data.get('semester')
            section = form.cleaned_data.get('section')
            subject = form.cleaned_data.get('subject')
            return HttpResponseRedirect(reverse('App_main:taking-attendance',
                                                kwargs={'department': department, 'batch': batch, 'section': section,
                                                        'semester': semester, 'subject': subject}))

    content = {
        'form': form,
    }
    return render(request, 'teachers/attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def taking_attendance(request, department, batch, section, semester, subject):
    date = datetime.datetime.today().date()
    students = StudentModel.objects.filter(department=department, batch=batch, section=section)
    teacher = TeacherModel.objects.get(user=request.user)
    for student in students:
        attendance = AttendanceModel(teacher=teacher, student=student, department=department,
                                     batch=batch, semester=semester, section=section, subject=subject)
        if AttendanceModel.objects.filter(teacher=teacher, student=student, department=department,
                                          batch=batch, semester=semester, section=section, subject=subject,
                                          date=date).exists():
            pass
        else:
            attendance.save()
    students_attendance = AttendanceModel.objects.filter(teacher=teacher,
                                                         department=department,
                                                         batch=batch, semester=semester, section=section,
                                                         subject=subject, date=date)
    if request.method == 'POST':
        all_ids = request.POST.get('all_ids')
        student_list = list(map(str, all_ids.split(',')))
        student_list.pop()
        for i in student_list:
            student = students_attendance.get(student=i)
            student.status = True
            student.save()
        return HttpResponseRedirect(reverse('App_main:teacher-dashboard'))

    content = {
        'date': date,
        'subject': subject,
        'students': students_attendance,
    }
    return render(request, 'teachers/taking_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def batch_based_attendance(request):
    s_attendance = []
    semesters = []
    semester_dict = {}
    s_batch = ' '
    s_department = ' '
    if request.method == 'POST':
        s_batch = request.POST.get('q')
        s_department = request.POST.get('p')
        s_section = request.POST.get('s')
        s_attendance = AttendanceModel.objects.filter(batch=s_batch, department=s_department,
                                                      section=s_section).order_by('student__student_id', 'subject')
        semesters = list(set(s_attendance.values_list('semester').order_by('-semester', 'subject')))
        for semi in semesters:
            semi = str(semi)[2:5]
            a = s_attendance.filter(semester=semi).count()
            semester_dict[f'{semi}'] = int(a)

    content = {
        'batch': s_batch,
        'department': s_department,
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'teachers/semester_based_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def student_attendance_record(request):
    s_attendance = []
    semesters = []
    semester_dict = {}
    if request.method == 'POST':
        s_id = request.POST.get('q')
        s_attendance = AttendanceModel.objects.filter(student__student_id=s_id)
        semesters = list(set(s_attendance.values_list('semester').order_by('-semester', 'subject')))
        for semi in semesters:
            semi = str(semi)[2:5]
            a = s_attendance.filter(semester=semi).count()
            b = s_attendance.filter(semester=semi, status=True).count()
            semester_dict[f'{semi}'] = int((b / a) * 100)

    content = {
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'teachers/student_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def semester_attendance_delete(request, semester, batch, department):
    attendance = AttendanceModel.objects.filter(department=department, batch=batch, semester=semester)
    for i in attendance:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:batch-based-attendance'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def take_exam(request):
    form = TestModelForm()
    if request.method == 'POST':
        form = TestModelForm(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            test.test_provider = request.user
            test.save()
            students = StudentModel.objects.filter(batch=test.batch, department=test.department,
                                                   section=test.section)
            for student in students:
                a = TestSubmissionModel(submitted_by=student, my_test=test)
                a.save()
            return HttpResponseRedirect(reverse('App_main:test-submissions'))
    content = {
        'form': form,
    }
    return render(request, 'teachers/take_exam.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def submitted_test_papers(request):
    tests = list(
        set(TestModel.objects.filter(test_provider=request.user).values_list('Title').order_by('-deadline')))
    test_ids = list(
        set(TestModel.objects.filter(test_provider=request.user).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(my_test__test_provider=request.user, status=True).order_by(
        '-my_test__deadline', '-marks')

    content = {
        'tests': tests,
        'submissions': submitted,
    }
    return render(request, 'teachers/submitted_test_papers.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def delete_tests(request, pk):
    tests = TestModel.objects.filter(Title=pk)
    for i in tests:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:test-submissions'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def update_test_marks(request, pk):
    mark = request.POST.get('marks')
    test = TestSubmissionModel.objects.get(id=pk)
    test.marks = mark
    test.save()
    return HttpResponseRedirect(reverse('App_main:test-submissions'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def test_results(request):
    t = {}
    tests = list(
        set(TestModel.objects.filter(test_provider=request.user).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(my_test__test_provider=request.user, status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
    }
    return render(request, 'teachers/test_results.html', context=content)


# -----------------------------------------------------------------------------------------------------------------------


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = StudentModel.objects.get(user=request.user)
    content = {
        'date': date,
        'profile': profile,
    }
    return render(request, 'students/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def submit_assignments(request):
    student = StudentModel.objects.get(user=request.user)
    assignments = list(
        set(AssignmentSubmissionModel.objects.filter(submitted_by=student, status=False).values_list(
            'my_assignment__Title').order_by('my_assignment__deadline')))
    submitted = AssignmentSubmissionModel.objects.filter(submitted_by=student, status=False).order_by(
        '-my_assignment__deadline', '-created')

    content = {
        'assignments': assignments,
        'submissions': submitted,
    }
    return render(request, 'students/submit_assignments.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def update_assignment_file(request, pk):
    file = request.FILES.get('file')
    assignment = AssignmentSubmissionModel.objects.get(id=pk)
    assignment.submission_file = file
    assignment.status = True
    assignment.save()
    return HttpResponseRedirect(reverse('App_main:submit-assignments'))


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def submit_assignment_marks(request):
    student = StudentModel.objects.get(user=request.user)
    assignments = list(
        set(AssignmentSubmissionModel.objects.filter(submitted_by=student, status=True).values_list(
            'my_assignment__Title').order_by('my_assignment__deadline')))
    submitted = AssignmentSubmissionModel.objects.filter(submitted_by=student, status=True).order_by(
        '-my_assignment__deadline', '-created')
    content = {
        'assignments': assignments,
        'submissions': submitted,
    }
    return render(request, 'students/assignment_marks.html', context=content)
