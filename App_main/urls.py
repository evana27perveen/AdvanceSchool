from django.urls import path
from . import views

app_name = 'App_main'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-dept-students/<str:pk>/<str:dept>/', views.admin_specific_dept_students, name='admin-dept-students'),
    path('admin-student-disable/<int:k>/', views.admin_student_disable, name='admin-student-disable'),
    path('admin-student-activate/<int:k>/', views.admin_student_activate, name='admin-student-activate'),
    path('admin-new-routine', views.admin_publish_routine, name='admin-new-routine'),
    path('admins-routine', views.admins_routine, name='admins-routine'),
    path('admin-delete-routine/<int:pk>/', views.admin_delete_routine, name='admin-delete-routine'),
    path('admin-new-notice/', views.admin_publish_notice, name='admin-new-notice'),
    path('admin-all-notices/', views.admin_all_notices, name='admin-all-notices'),
    path('admin-delete-notice/<int:pk>/', views.admin_delete_notice, name='admin-delete-notice'),
    path('admin-batch-based-attendance/', views.admin_batch_based_attendance, name='admin-batch-based-attendance'),
    path('admin-semester-attendance-delete/<str:semester>/<str:batch>/<str:department>/',
         views.admin_semester_attendance_delete,
         name='admin-semester-attendance-delete'),
    path('admin-student-attendance-record/', views.admin_student_attendance_record,
         name='admin-student-attendance-record'),
    path('admin-merit-list/', views.admin_test_results, name='admin-merit-list'),
    path('admin-delete-tests/<str:pk>/', views.admin_delete_tests, name='admin-delete-test'),
    path('admin-salary-distribution/', views.admin_salary_distribution, name='admin-salary-distribution'),
    path('admin-student-batch-dept/', views.student_batch_dept, name='admin-student-batch-dept'),
    path('admin-student-fees/<str:batch>/<str:dept>/', views.admin_student_fees, name='admin-student-fees'),
    path('admin-each-salary-record/<int:pk>/', views.admin_each_salary_record,
         name='admin-each-salary-record'),

    # admin end-----------------------------------------------------------------------------------------------
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
    path('new-routine', views.publish_routine, name='new-routine'),
    path('teachers-routine', views.teachers_routine, name='teachers-routine'),
    path('delete-routine/<int:pk>/', views.delete_routine, name='delete-routine'),
    path('new-notice/', views.publish_notice, name='new-notice'),
    path('teacher-all-notices/', views.teacher_all_notices, name='teacher-all-notices'),
    path('delete-notice/<int:pk>/', views.delete_notice, name='delete-notice'),

    # teacher end-----------------------------------------------------------------------------------------------
    # student start----------------------------------------------------------------------------------------------

    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('submit-assignments/', views.submit_assignments, name='submit-assignments'),
    path('submit-file-assignment/<int:pk>/', views.update_assignment_file, name='submit-file-assignment'),
    path('assignment-marks/', views.submit_assignment_marks, name='assignment-marks'),
    path('student-attendance/', views.student_attendance, name='student-attendance'),
    path('student-routine/', views.students_routine, name='student-routine'),
    path('attend-exam/', views.attend_exam, name='attend-exam'),
    path('submit-test/<int:pk>/', views.submit_test, name='submit-test'),
    path('test-marks', views.test_marks, name='test-marks'),
    path('student-merit-list/', views.student_merit_list, name='student-merit-list'),
    path('student-all-notices/', views.student_all_notices, name='student-all-notices'),
    path('student-borrowed-books/', views.student_borrowed_books, name='student-borrowed-books'),
    path('student-borrow-records/', views.student_borrow_records, name='student-borrow-records'),
    path('student-monthly-fees/', views.student_monthly_fees, name='student-monthly-fees'),

    # Student end-----------------------------------------------------------------------------------------------
    # Accountant start----------------------------------------------------------------------------------------------

    path('accountant-dashboard/', views.accountant_dashboard, name='accountant-dashboard'),
    path('salary-list/', views.salary_list, name='salary-list'),
    path('salary-distribution/', views.salary_distribution, name='salary-distribution'),
    path('give-salary/<int:pk>/', views.provide_each_salary, name='give-salary'),
    path('student-fees/<str:batch>/<str:dept>/', views.student_fees, name='student-fees'),
    path('fee-approval/<int:pk>/', views.fee_approval, name='fee-approval'),
    path('accountant-all-notices/', views.accountant_all_notices, name='accountant-all-notices'),
    path('accountant-see-merit-list/', views.accountant_see_test_results, name='accountant-see-merit-list'),
    path('accountant-student-batch-dept/', views.accountant_student_batch_dept, name='accountant-student-batch-dept'),
    path('accountant-student-fees/<str:batch>/<str:dept>/', views.accountant_student_fees,
         name='accountant-student-fees'),
    path('accountant-each-salary-record/<int:pk>/', views.accountant_each_salary_record,
         name='accountant-each-salary-record'),

    # Accountant end-----------------------------------------------------------------------------------------------
    # Librarian start----------------------------------------------------------------------------------------------

    path('librarian-dashboard/', views.librarian_dashboard, name='librarian-dashboard'),
    path('book-category/', views.categories, name='book-category'),
    path('book-location/', views.locations, name='book-location'),
    path('all-book/', views.books, name='all-book'),
    path('cat-books/<str:cat>/', views.cat_books, name='cat-books'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete-category'),
    path('delete-location/<int:pk>/', views.delete_location, name='delete-location'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete-book'),
    path('book-details/<int:pk>/', views.book_view, name='book-details'),
    path('book-borrow/<int:pk>/', views.borrow, name='book-borrow'),
    path('book-return/<int:pk>/', views.return_book, name='book-return'),
    path('all-borrows/', views.all_borrows, name='all-borrows'),
    path('borrowed-books/', views.borrowed_books, name='borrowed-books'),
    path('librarian-all-notices/', views.librarian_all_notices, name='librarian-all-notices'),
    path('librarian-see-merit-list/', views.librarian_see_test_results, name='librarian-see-merit-list'),

    # Librarian end------------------------------------------------------------------------------------------------
    # Parent Start-----------------------------------------------------------------------------------------------
    path('parent-dashboard/', views.parent_dashboard, name='parent-dashboard'),
    path('parent-student-attendance-record/<int:pk>/', views.parent_student_attendance_record,
         name='parent-student-attendance-record'),
    path('parent-see-merit-list/', views.parent_see_test_results, name='parent-see-merit-list'),
    path('parent-borrowed-books/<int:pk>/', views.parent_borrowed_books, name='parent-borrowed-books'),
    path('parent-borrow-records/<int:pk>/', views.parent_borrow_records, name='parent-borrow-records'),
    path('parent-monthly-fees/<int:pk>/', views.parent_monthly_fees, name='parent-monthly-fees'),
    path('parent-all-notices/', views.parent_all_notices, name='parent-all-notices'),

    # Parent end-----------------------------------------------------------------------------------------------
    # Staff start-----------------------------------------------------------------------------------------------

    path('staff-dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('staff-see-merit-list/', views.staff_see_test_results, name='staff-see-merit-list'),
]
