from django.urls import path
from . import views

app_name = 'App_main'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    # teacher start-----------------------------------------------------------------------------------------------
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('specific-department-students/<str:pk>/<str:dept>/', views.specific_dept_students,
         name='specific-dept-students'),
    path('student-disable/<int:k>/', views.student_disable, name='student-disable'),
    path('student-activate/<int:k>/', views.student_activate, name='student-activate'),
    path('new-assignment/', views.new_assignment, name='new-assignment'),
    path('assignment-submissions/', views.submitted_assignments, name='assignment-submissions'),
    path('delete-assignment/<str:pk>/', views.delete_assignments, name='delete-assignment'),
    path('assignment-marks/<int:pk>/', views.update_assignment_marks, name='update-assign-mark'),
    path('take-attendance/', views.take_attendance, name='take-attendance'),
    path('taking-attendance/<str:department>/<str:batch>/<str:section>/<str:semester>/<str:subject>/',
         views.taking_attendance, name='taking-attendance'),
    path('batch-based-attendance/', views.batch_based_attendance, name='batch-based-attendance'),
    path('student-attendance-record/', views.student_attendance_record, name='student-attendance-record'),
    path('semester-attendance-delete/<str:semester>/<str:batch>/<str:department>/', views.semester_attendance_delete,
         name='semester-attendance-delete'),
    path('take-exam/', views.take_exam, name='take-exam'),
    path('test-submissions/', views.submitted_test_papers, name='test-submissions'),
    path('delete-tests/<str:pk>/', views.delete_tests, name='delete-test'),
    path('test-marks/<int:pk>/', views.update_test_marks, name='update-test-mark'),
    path('merit-list/', views.test_results, name='merit-list'),

    # teacher end-----------------------------------------------------------------------------------------------
    # student start----------------------------------------------------------------------------------------------

    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('submit-assignments/', views.submit_assignments, name='submit-assignments'),
    path('submit-file-assignment/<int:pk>/', views.update_assignment_file, name='submit-file-assignment'),
    path('assignment-marks/', views.submit_assignment_marks, name='assignment-marks'),

]
