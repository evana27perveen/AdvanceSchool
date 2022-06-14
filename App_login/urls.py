from django.urls import path
from . import views


app_name = 'App_login'

urlpatterns = [
    path('teacher-signup/', views.teacher_signup, name='teacher-signup'),
    path('student-signup/', views.student_signup, name='student-signup'),
    path('parent-signup/', views.parent_signup, name='parent-signup'),
    path('staff-signup/', views.staff_signup, name='staff-signup'),
    path('librarian-signup/', views.librarian_signup, name='librarian-signup'),
    path('accountant-signup/', views.accountant_signup, name='accountant-signup'),
    path('login/', views.login_system, name='login'),
    path('logout/', views.logout_system, name='logout'),

]
