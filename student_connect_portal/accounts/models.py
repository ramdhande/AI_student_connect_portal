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

    def __str__(self):
        return f"{self.username} ({self.role})"