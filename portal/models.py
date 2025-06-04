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

    Attributes:
        username (CharField): Unique username, max length 150 characters.
        is_active (BooleanField): Whether the user is active.
        is_staff (BooleanField): Whether the user has admin access.
        date_joined (DateTimeField): When the user was created.
    """
    username = models.CharField(max_length=150, unique=True)
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
        """Return string representation of the teacher."""
        return self.username

class Student(models.Model):
    """
    Model representing a student with name, subject, and marks.

    Attributes:
        name (CharField): Student's name, max length 100 characters.
        subject (CharField): Subject name, max length 100 characters.
        marks (IntegerField): Student's marks for the subject.
    """
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('name', 'subject')

    def __str__(self):
        """Return string representation of the student."""
        return f"{self.name} - {self.subject}"