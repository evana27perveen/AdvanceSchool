import calendar

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from App_login.models import TeacherModel, StudentModel, ParentModel, AccountantModel, LibrarianModel, \
    NonTeachingStaffModel, AdminModel
from App_main.forms import AssignmentForm, AttendanceModelForm, TestModelForm, AssignmentSubmissionForm, \
    RoutineModelForm, NoticeModelForm, CategoryForm, AddBookForm, BookBorrowForm, AddNewSelf
from App_main.models import AssignmentSubmissionModel, AssignmentModel, AttendanceModel, TestSubmissionModel, TestModel, \
    RoutineModel, NoticeModel, SalaryModel, ProvideSalaryModel, StudentFeesModel, MonthlyFeeModel, CategoryModel, \
    BookModel, BorrowModel, BookLocationModel


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


# --------------------------------------------------Admin-start---------------------------------------------------------


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    teacher = TeacherModel.objects.all().count()
    student = StudentModel.objects.all().count()
    parent = ParentModel.objects.all().count()
    accountant = AccountantModel.objects.all().count()
    librarian = LibrarianModel.objects.all().count()
    staff = NonTeachingStaffModel.objects.all().count()

    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))

    month = datetime.date.today().month
    year = datetime.date.today().year
    a_sum = []
    b_sum = []
    payable_salary = SalaryModel.objects.filter(status=True).values_list('salary')
    for i in payable_salary:
        i = str(i)[1:-2]
        a_sum.append(int(i))
    salary_to_pay = sum(a_sum)

    paid_slry = ProvideSalaryModel.objects.filter(status=True)
    for i in paid_slry:
        given_month = i.given.month
        given_year = i.given.year
        if given_month == month and given_year == year:
            salary_paid = i.salary.salary
            b_sum.append(salary_paid)
    paid_salary = sum(b_sum)

    to_pay = salary_to_pay - paid_salary
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    profile = AdminModel.objects.get(user=request.user)

    content = {
        'profile': profile,
        'salary_to_pay': salary_to_pay,
        'paid_salary': paid_salary,
        'to_pay': to_pay,
        'date': date,
        'month': calendar.month_name[month],
        'my_salary': a,
        'teacher': teacher,
        'student': student,
        'parent': parent,
        'accountant': accountant,
        'librarian': librarian,
        'staff': staff,
        'all_students': all_students.count(),
        'batch_list': batch_list,
    }
    return render(request, 'admins/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_specific_dept_students(request, pk, dept):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    dept = dept.lower()
    students = StudentModel.objects.filter(batch=pk, department=dept)
    content = {
        'students': students,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/dept_students.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_student_disable(request, k):
    student = StudentModel.objects.get(id=k)
    student.status = False
    student.save()
    pk = student.batch
    dept = student.department
    return HttpResponseRedirect(reverse('App_main:admin-dept-students', kwargs={'pk': pk, 'dept': dept}))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_student_activate(request, k):
    student = StudentModel.objects.get(id=k)
    student.status = True
    student.save()
    pk = student.batch
    dept = student.department
    return HttpResponseRedirect(reverse('App_main:admin-dept-students', kwargs={'pk': pk, 'dept': dept}))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_publish_routine(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    form = RoutineModelForm()
    if request.method == 'POST':
        form = RoutineModelForm(request.POST, request.FILES)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.save()
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    content = {
        'form': form,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/publish_routine.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admins_routine(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    semesters = []
    routines = RoutineModel.objects.all().order_by('semester', '-created')
    semester = list(set(routines.values_list('semester').order_by('semester')))
    for semi in semester:
        semi = str(semi)[2:5]
        semesters.append(semi)
    content = {
        'routines': routines,
        'semesters': semesters,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/routines.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_delete_routine(request, pk):
    routine = RoutineModel.objects.filter(id=pk)
    for i in routine:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:admins-routine'))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_publish_notice(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    form = NoticeModelForm()
    if request.method == 'POST':
        form = NoticeModelForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            return HttpResponseRedirect(reverse('App_main:admin-dashboard'))
    content = {
        'form': form,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/publish_notice.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_all_notices(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    notices = NoticeModel.objects.all().order_by('-created')
    content = {
        'notices': notices,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/notices.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_delete_notice(request, pk):
    notice = NoticeModel.objects.filter(id=pk)
    for i in notice:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:admin-all-notices'))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_batch_based_attendance(request):
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

    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'batch': s_batch,
        'department': s_department,
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'admins/semester_based_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_semester_attendance_delete(request, semester, batch, department):
    attendance = AttendanceModel.objects.filter(department=department, batch=batch, semester=semester)
    for i in attendance:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:admin-batch-based-attendance'))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_student_attendance_record(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'admins/student_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_test_results(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    t = {}
    tests = list(
        set(TestModel.objects.all().values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
    }
    return render(request, 'admins/test_results.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_delete_tests(request, pk):
    tests = TestModel.objects.filter(Title=pk)
    for i in tests:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:test-submissions'))


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_salary_distribution(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    salaries = SalaryModel.objects.filter(status=True)
    for s in salaries:
        try:
            slry = ProvideSalaryModel.objects.get(salary=s, given__month=month, given__year=year)
            pass
        except ObjectDoesNotExist:
            slry = ProvideSalaryModel(salary=s, status=False)
            slry.save()
    m_y = []
    salary_payment = ProvideSalaryModel.objects.all().order_by('given')
    month_year = list(salary_payment.values_list('given__year', 'given__month'))
    for i in month_year:
        ay = str(i[0])
        bm = i[1]
        m_y.append(str(calendar.month_name[bm]) + ' ' + ay)
    m_y = list(set(m_y))

    content = {
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'salary_payment': salary_payment,
        'm_y': m_y,
        'my_salary': a,
    }
    return render(request, 'admins/salary_distribution.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def student_batch_dept(request):
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'all_students': all_students.count(),
        'batch_list': batch_list,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/student_batch_dept.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_student_fees(request, batch, dept):
    batch = batch
    dept = dept
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year

    fees = StudentFeesModel.objects.filter(status=True, user__batch=batch, user__department=dept)
    for s in fees:
        try:
            fee = MonthlyFeeModel.objects.get(fee=s, created__month=month, created__year=year)
            pass
        except ObjectDoesNotExist:
            fee = MonthlyFeeModel(fee=s, status=False)
            fee.save()
    m_y = []
    fee_payment = MonthlyFeeModel.objects.filter(fee__user__department=dept, fee__user__batch=batch)
    month_year = list(fee_payment.values_list('created__year', 'created__month'))
    for i in month_year:
        ay = str(i[0])
        bm = i[1]
        m_y.append(str(calendar.month_name[bm]) + ' ' + ay)
    m_y = list(set(m_y))
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'batch': batch,
        'dept': dept,
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'fee_payment': fee_payment,
        'm_y': m_y,
        'my_salary': a,
    }
    return render(request, 'admins/student_fees.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_admin)
def admin_each_salary_record(request, pk):
    salaries = ProvideSalaryModel.objects.filter(salary__user_id=pk)
    fixed = SalaryModel.objects.get(user_id=pk)
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'salaries': salaries,
        'fixed': fixed,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'admins/admin_each_salary_record.html', context=content)


# --------------------------------------------------Admin-end-----------------------------------------------------------
# -------------------------------------------------Teacher-start--------------------------------------------------------


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = TeacherModel.objects.get(user=request.user)
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))

    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'date': date,
        'profile': profile,
        'all_students': all_students.count(),
        'batch_list': batch_list,
    }
    return render(request, 'teachers/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def specific_dept_students(request, pk, dept):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    dept = dept.lower()
    students = StudentModel.objects.filter(batch=pk, department=dept)
    content = {
        'students': students,
        'my_salary': a,
        'month': calendar.month_name[month],
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
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'teachers/new_assignment.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def submitted_assignments(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    assignments = list(
        set(AssignmentModel.objects.filter(provider=request.user).values_list('Title').order_by('deadline')))
    submitted = AssignmentSubmissionModel.objects.filter(my_assignment__provider=request.user, status=True).order_by(
        '-my_assignment__deadline', '-created')

    content = {
        'assignments': assignments,
        'submissions': submitted,
        'my_salary': a,
        'month': calendar.month_name[month],
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
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'teachers/attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def taking_attendance(request, department, batch, section, semester, subject):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
        'date': date,
        'subject': subject,
        'students': students_attendance,
    }
    return render(request, 'teachers/taking_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def batch_based_attendance(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
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
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
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
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
    }
    return render(request, 'teachers/take_exam.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def submitted_test_papers(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    tests = list(
        set(TestModel.objects.filter(test_provider=request.user).values_list('Title').order_by('-deadline')))
    test_ids = list(
        set(TestModel.objects.filter(test_provider=request.user).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(my_test__test_provider=request.user, status=True).order_by(
        '-my_test__deadline', '-marks')

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
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
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
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
        'my_salary': a,
        'month': calendar.month_name[month],
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
    }
    return render(request, 'teachers/test_results.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def publish_routine(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    form = RoutineModelForm()
    if request.method == 'POST':
        form = RoutineModelForm(request.POST, request.FILES)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.save()
            return HttpResponseRedirect(reverse('App_main:teacher-dashboard'))
    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
    }
    return render(request, 'teachers/publish_routine.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def teachers_routine(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    semesters = []
    routines = RoutineModel.objects.all().order_by('semester', '-created')
    semester = list(set(routines.values_list('semester').order_by('semester')))
    for semi in semester:
        semi = str(semi)[2:5]
        semesters.append(semi)
    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'routines': routines,
        'semesters': semesters,
    }
    return render(request, 'teachers/routines.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def delete_routine(request, pk):
    routine = RoutineModel.objects.filter(id=pk)
    for i in routine:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:teachers-routine'))


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def publish_notice(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    form = NoticeModelForm()
    if request.method == 'POST':
        form = NoticeModelForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.user = request.user
            notice.save()
            return HttpResponseRedirect(reverse('App_main:teacher-dashboard'))
    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
    }
    return render(request, 'teachers/publish_notice.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def teacher_all_notices(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    notices = NoticeModel.objects.all().order_by('-created')
    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'notices': notices,
    }
    return render(request, 'teachers/notices.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_teacher)
def delete_notice(request, pk):
    notice = NoticeModel.objects.filter(id=pk)
    for i in notice:
        i.delete()
    return HttpResponseRedirect(reverse('App_main:teacher-all-notices'))


# ----------------------------------------------------Teacher-end-------------------------------------------------------
# ----------------------------------------------------Student-start-----------------------------------------------------


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


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_attendance(request):
    student = StudentModel.objects.get(user=request.user)
    semester_dict = {}
    s_attendance = AttendanceModel.objects.filter(student=student).order_by('semester', 'subject')
    semesters = list(set(s_attendance.values_list('semester').order_by('semester', 'subject')))
    for semi in semesters:
        semi = str(semi)[2:5]
        a = s_attendance.filter(semester=semi).count()
        b = s_attendance.filter(semester=semi, status=True).count()
        semester_dict[f'{semi}'] = zip(f'{int(a)}', {int((b / a) * 100)})

    content = {
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'students/student_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def students_routine(request):
    student = StudentModel.objects.get(user=request.user)
    semesters = []
    routines = RoutineModel.objects.filter(department=student.department, batch=student.batch,
                                           section=student.section).order_by('semester', '-created')
    semester = list(set(routines.values_list('semester').order_by('semester')))
    for semi in semester:
        semi = str(semi)[2:5]
        semesters.append(semi)
    content = {
        'routines': routines,
        'semesters': semesters,
    }
    return render(request, 'students/routines.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def attend_exam(request):
    student = StudentModel.objects.get(user=request.user)
    tests = list(
        set(TestModel.objects.filter(department=student.department, batch=student.batch,
                                     section=student.section, my_test__submitted_by=student,
                                     my_test__status=False).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(submitted_by=student, status=False).order_by(
        '-my_test__deadline', '-marks')

    content = {
        'tests': tests,
        'submissions': submitted,
    }
    return render(request, 'students/attend_test.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def submit_test(request, pk):
    ans_file = request.POST.get('ans_file')
    test = TestSubmissionModel.objects.get(id=pk)
    test.submission_file = ans_file
    test.status = True
    test.save()
    return HttpResponseRedirect(reverse('App_main:attend-exam'))


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def test_marks(request):
    student = StudentModel.objects.get(user=request.user)
    tests = list(
        set(TestModel.objects.filter(department=student.department, batch=student.batch,
                                     section=student.section, my_test__submitted_by=student,
                                     my_test__status=False).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(submitted_by=student, status=False).order_by(
        '-my_test__deadline')

    content = {
        'tests': tests,
        'submissions': submitted,
    }
    return render(request, 'students/test_marks.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_merit_list(request):
    t = {}
    student = StudentModel.objects.get(user=request.user)
    tests = list(
        set(TestModel.objects.filter(department=student.department, batch=student.batch,
                                     section=student.section, my_test__submitted_by=student,
                                     my_test__status=True).values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(my_test__department=student.department, my_test__batch=student.batch,
                                                   my_test__section=student.section, status=True).order_by('-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
    }
    return render(request, 'students/merit_list.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_all_notices(request):
    notices = NoticeModel.objects.all().order_by('-created')
    content = {
        'notices': notices,
    }
    return render(request, 'students/notices.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_borrowed_books(request):
    borrows = BorrowModel.objects.filter(user__user=request.user, status=True).order_by('-date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'students/borrowed_books.html', context=content)

@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_borrow_records(request):
    borrows = BorrowModel.objects.filter(user__user=request.user).order_by('-date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'students/student_borrow_records.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_student)
def student_monthly_fees(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year
    fees = StudentFeesModel.objects.get(user__user=request.user)
    m_fee = MonthlyFeeModel.objects.filter(fee=fees).order_by('-created')

    content = {
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'fee_payment': m_fee,
        'fees': fees,

    }
    return render(request, 'students/monthly_student_fees.html', context=content)


# -----------------------------------------------Student-end------------------------------------------------------------
# ---------------------------------------------Accountant-start---------------------------------------------------------


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_dashboard(request):
    profile = AccountantModel.objects.get(user=request.user)
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a_sum = []
    b_sum = []
    payable_salary = SalaryModel.objects.filter(status=True).values_list('salary')
    for i in payable_salary:
        i = str(i)[1:-2]
        a_sum.append(int(i))
    salary_to_pay = sum(a_sum)

    paid_slry = ProvideSalaryModel.objects.filter(status=True)
    for i in paid_slry:
        given_month = i.given.month
        given_year = i.given.year
        if given_month == month and given_year == year:
            salary_paid = i.salary.salary
            b_sum.append(salary_paid)
    paid_salary = sum(b_sum)

    to_pay = salary_to_pay - paid_salary
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'all_students': all_students.count(),
        'batch_list': batch_list,
        'salary_to_pay': salary_to_pay,
        'paid_salary': paid_salary,
        'to_pay': to_pay,
        'date': date,
        'month': calendar.month_name[month],
        'my_salary': a,
        'profile': profile,
    }
    return render(request, 'accountants/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def salary_list(request):
    salaries = SalaryModel.objects.filter(status=True)
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'salaries': salaries,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'accountants/salary_list.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def salary_distribution(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    salaries = SalaryModel.objects.filter(status=True)
    for s in salaries:
        try:
            slry = ProvideSalaryModel.objects.get(salary=s, given__month=month, given__year=year)
            pass
        except ObjectDoesNotExist:
            slry = ProvideSalaryModel(salary=s, status=False)
            slry.save()
    m_y = []
    salary_payment = ProvideSalaryModel.objects.all().order_by('given')
    month_year = list(salary_payment.values_list('given__year', 'given__month'))
    for i in month_year:
        ay = str(i[0])
        bm = i[1]
        m_y.append(str(calendar.month_name[bm]) + ' ' + ay)
    m_y = list(set(m_y))

    content = {
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'salary_payment': salary_payment,
        'm_y': m_y,
        'my_salary': a,
    }
    return render(request, 'accountants/salary_distribution.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def provide_each_salary(request, pk):
    salary = ProvideSalaryModel.objects.get(id=pk)
    salary.status = True
    salary.save()
    return HttpResponseRedirect(reverse('App_main:salary-distribution'))


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def student_fees(request, batch, dept):
    batch = batch
    dept = dept
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year

    fees = StudentFeesModel.objects.filter(status=True, user__batch=batch, user__department=dept)
    for s in fees:
        try:
            fee = MonthlyFeeModel.objects.get(fee=s, created__month=month, created__year=year)
            pass
        except ObjectDoesNotExist:
            fee = MonthlyFeeModel(fee=s, status=False)
            fee.save()
    m_y = []
    fee_payment = MonthlyFeeModel.objects.filter(fee__user__department=dept, fee__user__batch=batch)
    month_year = list(fee_payment.values_list('created__year', 'created__month'))
    for i in month_year:
        ay = str(i[0])
        bm = i[1]
        m_y.append(str(calendar.month_name[bm]) + ' ' + ay)
    m_y = list(set(m_y))
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'batch': batch,
        'dept': dept,
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'fee_payment': fee_payment,
        'm_y': m_y,
        'my_salary': a,
    }
    return render(request, 'accountants/student_fees.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def fee_approval(request, pk):
    fee = MonthlyFeeModel.objects.get(id=pk)
    fee.status = True
    fee.save()
    student_fee = StudentFeesModel.objects.get(user=fee.fee.user)
    student_fee.fee_counter += 1
    if student_fee.fee_counter == 48:
        student_fee.status = False
    student_fee.save()
    batch = student_fee.user.batch
    dept = student_fee.user.department
    return HttpResponseRedirect(reverse('App_main:student-fees', kwargs={'batch': batch, 'dept': dept}))


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_all_notices(request):
    notices = NoticeModel.objects.all().order_by('-created')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'notices': notices,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'accountants/notices.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_see_test_results(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    t = {}
    tests = list(
        set(TestModel.objects.all().values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'accountants/test_results.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_student_batch_dept(request):
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'all_students': all_students.count(),
        'batch_list': batch_list,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'accountants/student_batch_dept.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_student_fees(request, batch, dept):
    batch = batch
    dept = dept
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year

    fees = StudentFeesModel.objects.filter(status=True, user__batch=batch, user__department=dept)
    for s in fees:
        try:
            fee = MonthlyFeeModel.objects.get(fee=s, created__month=month, created__year=year)
            pass
        except ObjectDoesNotExist:
            fee = MonthlyFeeModel(fee=s, status=False)
            fee.save()
    m_y = []
    fee_payment = MonthlyFeeModel.objects.filter(fee__user__department=dept, fee__user__batch=batch)
    month_year = list(fee_payment.values_list('created__year', 'created__month'))
    for i in month_year:
        ay = str(i[0])
        bm = i[1]
        m_y.append(str(calendar.month_name[bm]) + ' ' + ay)
    m_y = list(set(m_y))
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'batch': batch,
        'dept': dept,
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'fee_payment': fee_payment,
        'm_y': m_y,
        'my_salary': a,
    }
    return render(request, 'accountants/accountant_student_fees.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_accountant)
def accountant_each_salary_record(request, pk):
    salaries = ProvideSalaryModel.objects.filter(salary__user_id=pk)
    fixed = SalaryModel.objects.get(user_id=pk)
    month = datetime.date.today().month
    year = datetime.date.today().year

    slries = SalaryModel.objects.filter(status=True)
    for s in slries:
        try:
            slry = ProvideSalaryModel.objects.get(salary=s, given__month=month, given__year=year)
            pass
        except ObjectDoesNotExist:
            slry = ProvideSalaryModel(salary=s, status=False)
            slry.save()

    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'salaries': salaries,
        'fixed': fixed,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'accountants/accountant_each_salary_record.html', context=content)


# -----------------------------------------------Accountant-end---------------------------------------------------------
# -----------------------------------------------Librarian-start--------------------------------------------------------


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def librarian_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = LibrarianModel.objects.get(user=request.user)
    all_students = StudentModel.objects.all()
    batch_list = all_students.values_list('batch')
    batch_list = list(set(batch_list))

    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'date': date,
        'profile': profile,
        'all_students': all_students.count(),
        'batch_list': batch_list,
    }
    return render(request, 'librarians/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def categories(request):
    book_count = []
    all_categories = CategoryModel.objects.all().order_by('title')
    all_books = BookModel.objects.all().order_by('title')
    for i in all_categories:
        c = all_books.filter(categories=i).count()
        book_count.append(c)
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    form = CategoryForm()
    if request.method == "POST" and 'new_cat':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            cat = form.save()
            return HttpResponseRedirect(reverse('App_main:book-category'))

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
        'cat_count': zip(all_categories, book_count)
    }

    return render(request, "librarians/category.html", context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def books(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    form = AddBookForm()
    if request.method == "POST" and 'add_book':
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect(reverse('App_main:all-book'))

    all_books = BookModel.objects.all().order_by('title')

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
        'all_books': all_books,
    }

    return render(request, "librarians/all_books.html", context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def delete_category(request, pk):
    category = CategoryModel.objects.get(id=pk)
    category.delete()
    return HttpResponseRedirect(reverse('App_main:book-category'))


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def delete_location(request, pk):
    loc = BookLocationModel.objects.get(id=pk)
    loc.delete()
    return HttpResponseRedirect(reverse('App_main:book-location'))


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def delete_book(request, pk):
    book = BookModel.objects.get(id=pk)
    book.delete()
    return HttpResponseRedirect(reverse('App_main:all-book'))


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def borrow(request, pk):
    book = BookModel.objects.get(id=pk)
    print(book)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = StudentModel.objects.get(student_id=student_id)
        bro = BorrowModel(book=book, user=student)
        try:
            record = BorrowModel.objects.get(book=book, user=student, status=True)
            return HttpResponseRedirect(reverse('App_main:book-borrow'))
        except ObjectDoesNotExist:
            bro.save()
            book.available -= 1
            book.save()
            return HttpResponseRedirect(reverse('App_main:book-borrow'))


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def book_view(request, pk):
    book = BookModel.objects.get(id=pk)
    borrows = BorrowModel.objects.filter(book=book).order_by('date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'book': book,
        'borrows': borrows,
    }
    return render(request, 'librarians/book_details.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def return_book(request, pk):
    borrow = BorrowModel.objects.get(id=pk)
    borrow.status = False
    borrow.save()
    book = BookModel.objects.get(id=borrow.book.id)
    book.available += 1
    book.save()
    this_pk = book.id
    return HttpResponseRedirect(reverse('App_main:book-details', kwargs={'pk': this_pk}))


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def all_borrows(request):
    borrows = BorrowModel.objects.all().order_by('date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'librarians/all_borrows.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def borrowed_books(request):
    borrows = BorrowModel.objects.filter(status=True).order_by('-date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'librarians/borrowed_books.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def cat_books(request, cat):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    category = CategoryModel.objects.get(title=cat)
    all_books = BookModel.objects.filter(categories=category).order_by('title')

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'all_books': all_books,
    }

    return render(request, "librarians/cat_books.html", context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def locations(request):
    book_count = []
    all_locations = BookLocationModel.objects.all().order_by('self_no')
    all_books = BookModel.objects.all().order_by('title')
    for i in all_locations:
        c = all_books.filter(location=i).count()
        book_count.append(c)
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'

    form = AddNewSelf()
    if request.method == "POST" and 'new_cat':
        form = AddNewSelf(data=request.POST)
        if form.is_valid():
            loc = form.save()
            return HttpResponseRedirect(reverse('App_main:book-location'))

    content = {
        'my_salary': a,
        'month': calendar.month_name[month],
        'form': form,
        'cat_count': zip(all_locations, book_count)
    }

    return render(request, "librarians/location.html", context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def librarian_all_notices(request):
    notices = NoticeModel.objects.all().order_by('-created')
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    content = {
        'notices': notices,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'librarians/notices.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_librarian)
def librarian_see_test_results(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    t = {}
    tests = list(
        set(TestModel.objects.all().values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'librarians/test_results.html', context=content)


# ---------------------------------------------Librarian-end------------------------------------------------------------
# ----------------------------------------------Parent-start------------------------------------------------------------

@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = ParentModel.objects.get(user=request.user)

    month = datetime.date.today().month
    year = datetime.date.today().year

    content = {
        'month': calendar.month_name[month],
        'date': date,
        'profile': profile,
    }
    return render(request, 'parents/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_student_attendance_record(request, pk):
    month = datetime.date.today().month
    year = datetime.date.today().year
    s_attendance = []
    semesters = []
    semester_dict = {}
    s_attendance = AttendanceModel.objects.filter(student__student_id=pk)
    semesters = list(set(s_attendance.values_list('semester').order_by('-semester', 'subject')))
    for semi in semesters:
        semi = str(semi)[2:5]
        a = s_attendance.filter(semester=semi).count()
        b = s_attendance.filter(semester=semi, status=True).count()
        semester_dict[f'{semi}'] = int((b / a) * 100)
    profile = ParentModel.objects.get(user=request.user)
    content = {
        'profile': profile,
        'month': calendar.month_name[month],
        'semester_dict': zip(semester_dict.keys(), semester_dict.values()),
        'semesters': semesters,
        's_attendance': s_attendance,
    }
    return render(request, 'parents/student_attendance.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_see_test_results(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    t = {}
    tests = list(
        set(TestModel.objects.all().values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id
    profile = ParentModel.objects.get(user=request.user)
    content = {
        'profile': profile,
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
        'month': calendar.month_name[month],
    }
    return render(request, 'parents/test_results.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_borrowed_books(request, pk):
    borrows = BorrowModel.objects.filter(user__student_id=pk, status=True).order_by('-date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    profile = ParentModel.objects.get(user=request.user)
    content = {
        'profile': profile,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'parents/borrowed_books.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_borrow_records(request, pk):
    borrows = BorrowModel.objects.filter(user__student_id=pk).order_by('-date')
    month = datetime.date.today().month
    year = datetime.date.today().year
    profile = ParentModel.objects.get(user=request.user)
    content = {
        'profile': profile,
        'month': calendar.month_name[month],
        'borrows': borrows,
    }
    return render(request, 'parents/student_borrow_records.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_monthly_fees(request, pk):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    month = datetime.date.today().month
    year = datetime.date.today().year
    fees = StudentFeesModel.objects.get(user__student_id=pk)
    m_fee = MonthlyFeeModel.objects.filter(fee=fees).order_by('-created')
    profile = ParentModel.objects.get(user=request.user)
    content = {
        'profile': profile,
        'date': date,
        'month': calendar.month_name[month],
        'year': year,
        'fee_payment': m_fee,
        'fees': fees,

    }
    return render(request, 'parents/monthly_student_fees.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_parent)
def parent_all_notices(request):
    notices = NoticeModel.objects.all().order_by('-created')
    month = datetime.date.today().month
    year = datetime.date.today().year

    profile = ParentModel.objects.get(user=request.user)

    content = {
        'profile': profile,
        'notices': notices,
        'month': calendar.month_name[month],
    }
    return render(request, 'parents/notices.html', context=content)

# ------------------------------------------------Parent-end------------------------------------------------------------
# ------------------------------------------------Staff-start-----------------------------------------------------------

@login_required(login_url='App_login:login')
@user_passes_test(is_staff)
def staff_dashboard(request):
    date = datetime.datetime.now().strftime('%A %d. %B %Y')
    profile = NonTeachingStaffModel.objects.get(user=request.user)
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    notices = NoticeModel.objects.all().order_by('-created')
    content = {
        'notices': notices,
        'my_salary': a,
        'month': calendar.month_name[month],
        'date': date,
        'profile': profile,
    }
    return render(request, 'staff/dashboard.html', context=content)


@login_required(login_url='App_login:login')
@user_passes_test(is_staff)
def staff_see_test_results(request):
    month = datetime.date.today().month
    year = datetime.date.today().year
    a = ''
    try:
        my_salary = ProvideSalaryModel.objects.get(salary__user=request.user, status=True)
        if my_salary.given.month == month and my_salary.given.year == year:
            a = 'Paid'
    except ObjectDoesNotExist:
        a = 'Pending'
    t = {}
    tests = list(
        set(TestModel.objects.all().values_list('Title').order_by('-deadline')))
    submitted = TestSubmissionModel.objects.filter(status=True).order_by(
        '-marks')
    for test in tests:
        test = str(test)[2:-3]
        test_id = TestModel.objects.get(Title=test)
        t[f'{test}'] = test_id.id

    content = {
        'tests': zip(t.keys(), t.values()),
        'submissions': submitted,
        'my_salary': a,
        'month': calendar.month_name[month],
    }
    return render(request, 'staff/test_results.html', context=content)


# -------------------------------------------------Staff-end------------------------------------------------------------

