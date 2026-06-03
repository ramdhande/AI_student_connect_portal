from django.contrib.auth.models import AbstractUser
from django.db import models


class StudentProfile(models.Model):
    """
    Stores official student records provided by the college.
    This acts as the institutional database.
    Only students present here can register accounts.
    """

    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class TeacherProfile(models.Model):
    """
    Stores official teacher records.
    Only teachers present here can register accounts.
    """
    teacher_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"


class ParentProfile(models.Model):
    """
    Stores official parent records.
    Only parents present here can register accounts.
    """
    parent_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    linked_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='parents')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.parent_id} - {self.full_name}"


class StudentProgress(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='progress_records')
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    grade = models.CharField(max_length=5)
    semester = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject}: {self.marks} ({self.grade})"


class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.CharField(max_length=100)
    percentage = models.IntegerField()
    total_classes = models.IntegerField(default=40)
    classes_attended = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject}: {self.percentage}%"


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Links login credentials with StudentProfile to ensure
    only verified students can create accounts.
    """

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    student_profile = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_account'
    )

    teacher_profile = models.OneToOneField(
        TeacherProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_account'
    )

    parent_profile = models.OneToOneField(
        ParentProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_account'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"