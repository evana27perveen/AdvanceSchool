from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from App_login.models import StudentModel, TeacherModel

dept = (
    ('cse', 'CSE'),
    ('bba', 'BBA'),
    ('bthm', 'BTHM'),
)

subjects = (
    ('Introduction To Computer', 'Introduction To Computer'),
    ('Programming Language', 'Programming Language'),
    ('Web Engineering', 'Web Engineering'),
    ('Image Processing', 'Image Processing'),
)

batches = (
    ('Select One', 'Select One'),
    ('16th', '16th'),
    ('17th', '17th'),
    ('18th', '18th'),
    ('19th', '19th'),
    ('20th', '20th'),
    ('21st', '21st'),
    ('22nd', '22nd'),
    ('23rd', '23rd'),
    ('24th', '24th'),
    ('25th', '25th'),
    ('26th', '26th'),
    ('27th', '27th'),
)

semesters = (
    ('Select One', 'Select One'),
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),
    ('6th', '6th'),
    ('7th', '7th'),
    ('8th', '8th'),
)

sec = (
    ('Select One', 'Select One'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)


class AssignmentModel(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_provider')
    department = models.CharField(choices=dept, max_length=50)
    batch = models.CharField(choices=batches, max_length=50)
    section = models.CharField(choices=sec, max_length=10, default='Select One')
    semester = models.CharField(choices=semesters, max_length=50)
    subject = models.CharField(choices=subjects, max_length=100)
    Title = models.CharField(max_length=500)
    assignment = models.FileField(upload_to='assignments/')
    created = models.DateField(auto_now=True)
    deadline = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.batch}-{self.department}-{self.section}-{self.Title}"


class AssignmentSubmissionModel(models.Model):
    submitted_by = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='student_submit')
    my_assignment = models.ForeignKey(AssignmentModel, on_delete=models.CASCADE, related_name='my_assignment')
    submission_file = models.FileField(upload_to='submitted_assignments/', blank=True)
    created = models.DateField(auto_now=True)
    marks = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submitted_by.student_id}-{self.my_assignment}"


class AttendanceModel(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.DO_NOTHING, related_name='course_teacher')
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='student_attendance', blank=True)
    department = models.CharField(choices=dept, max_length=50)
    batch = models.CharField(choices=batches, max_length=50)
    section = models.CharField(choices=sec, max_length=10)
    semester = models.CharField(choices=semesters, max_length=50)
    subject = models.CharField(choices=subjects, max_length=100)
    status = models.BooleanField(default=False, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.student.student_id}-{self.status}"


class TestModel(models.Model):
    test_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_holder')
    department = models.CharField(choices=dept, max_length=50)
    batch = models.CharField(choices=batches, max_length=50)
    section = models.CharField(choices=sec, max_length=10, default='Select One')
    semester = models.CharField(choices=semesters, max_length=50)
    subject = models.CharField(choices=subjects, max_length=100)
    Title = models.CharField(max_length=500)
    test_paper = models.FileField(upload_to='test_papers/')
    created = models.DateTimeField(auto_now=True)
    starting_time = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.BooleanField(default=True)
    total_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.batch}-{self.department}-{self.section}-{self.Title}"


class TestSubmissionModel(models.Model):
    submitted_by = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='test_submit_student')
    my_test = models.ForeignKey(TestModel, on_delete=models.CASCADE, related_name='my_test')
    submission_file = models.FileField(upload_to='submitted_tests/', blank=True)
    created = models.DateTimeField(auto_now=True)
    marks = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submitted_by.student_id}-{self.my_test}"

    def identify(self):
        return f"{self.my_test.batch} {self.my_test.department} {self.my_test.section} - {self.submitted_by.student_id}"
