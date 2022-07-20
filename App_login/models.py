from django.db import models
from django.contrib.auth.models import User, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

gender_choice = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Third Gender", "Third Gender"),
)

teaching_status = (
    ('Lecturer - Permanent', 'Lecturer - Permanent'),
    ('Lecturer - Guest', 'Lecturer - Guest'),
    ('Lecturer & Department-Head', 'Lecturer & Department-Head'),
    ('Assistant-Lecturer', 'Assistant-Lecturer'),
)

dept = (
    ('cse', 'CSE'),
    ('bba', 'BBA'),
    ('bthm', 'BTHM'),
)

sec = (
    ('Select One', 'Select One'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)


# Create your models here.

class AdminModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_user')
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    salary = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='admin_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_user')
    phone_number = PhoneNumberField(unique=True)
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    department = models.CharField(choices=dept, max_length=50)
    designation = models.CharField(choices=teaching_status, max_length=50)
    teacher_id = models.CharField(max_length=150, unique=True)
    salary = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='teacher_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class StudentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_user')
    phone_number = PhoneNumberField(unique=True)
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    student_id = models.CharField(max_length=150, unique=True)
    department = models.CharField(choices=dept, max_length=50)
    batch = models.CharField(max_length=50)
    section = models.CharField(choices=sec, max_length=10, default='Select One')
    tuition_fee = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='student_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def batch_dept(self):
        return f"{self.batch}-{self.department}"


class ParentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent_user')
    phone_number = PhoneNumberField()
    gender = models.CharField(choices=gender_choice, max_length=15)
    scholar = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='my_scholar')
    relation = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='parent_picture')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class NonTeachingStaffModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_user')
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    salary = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='staff_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class LibrarianModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian_user')
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    salary = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='librarian_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class AccountantModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accountant_user')
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, max_length=15)
    salary = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='accountant_picture')
    joining_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
