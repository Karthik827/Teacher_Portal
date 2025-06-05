from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class TeacherManager(BaseUserManager):
    """
    Custom manager for the Teacher model.

    Provides methods to create regular users and superusers.
    """
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and save a regular user with the given username and password.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            **extra_fields: Additional fields for the user.

        Returns:
            Teacher: The created user instance.
        """
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and save a superuser with the given username and password.

        Args:
            username (str): The username for the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the superuser.

        Returns:
            Teacher: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Teacher(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a teacher.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = TeacherManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.username

class Student(models.Model):
    """
    Model representing a student with name, subject, and marks.
    """
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    # If you want to add these fields:
    # email = models.EmailField(blank=True)
    # phone = models.CharField(max_length=15, blank=True)
    # teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self):
        return f"{self.name} - {self.subject}"
