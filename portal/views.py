from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Teacher, Student
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import re
import json
import os
import sys
import django
from django.conf import settings

def validate_input(data):
    pattern = r'^[a-zA-Z0-9\s]+$'
    for value in data.values():
        if isinstance(value, str) and not re.match(pattern, value):
            return False
    return True

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('portal:home')  # Use namespace
        return render(request, 'portal/register.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not validate_input({'username': username, 'password': password}):
                return JsonResponse({'error': 'Invalid input: Use only letters, numbers, and spaces'}, status=400)
            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
            if Teacher.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)

            teacher = Teacher.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('portal:home')  # Use namespace, changed from 'login' to avoid loop
        return render(request, 'portal/login.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not validate_input({'username': username, 'password': password}):
                return JsonResponse({'error': 'Invalid input'}, status=400)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('portal:login')  # Use namespace
        return render(request, 'portal/home.html')

class StudentListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('portal:login')  # Use namespace
        students = Student.objects.all().values('id', 'name', 'subject', 'marks')
        return JsonResponse(list(students), safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AddStudentView(View):
    @method_decorator(require_POST)
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        try:
            data = json.loads(request.body)
            name = data.get('name')
            subject = data.get('subject')
            marks = data.get('marks')

            # Check if all required fields are present
            if not name or not subject or marks is None:
                return JsonResponse({'error': 'Name, subject, and marks are required'}, status=400)

            if not validate_input({'name': name, 'subject': subject}):
                return JsonResponse({'error': 'Invalid input'}, status=400)

            try:
                marks = int(marks)
                if marks < 0 or marks > 100:
                    return JsonResponse({'error': 'Marks must be between 0 and 100'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid marks value'}, status=400)

            try:
                student = Student.objects.get(name=name, subject=subject)
                student.marks += marks
                student.save()
            except Student.DoesNotExist:
                Student.objects.create(name=name, subject=subject, marks=marks)
            return JsonResponse({'message': 'Student added/updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateStudentView(View):
    @method_decorator(require_POST)
    def post(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        try:
            data = json.loads(request.body)
            name = data.get('name')
            subject = data.get('subject')
            marks = data.get('marks')

            if not validate_input({'name': name, 'subject': subject}):
                return JsonResponse({'error': 'Invalid input'}, status=400)

            try:
                marks = int(marks)
                if marks < 0 or marks > 100:
                    return JsonResponse({'error': 'Marks must be between 0 and 100'}, status=400)
            except (ValueError, TypeError):
                return JsonResponse({'error': 'Invalid marks value'}, status=400)

            try:
                student = Student.objects.get(id=id)
                student.name = name
                student.subject = subject
                student.marks = marks
                student.save()
                return JsonResponse({'message': 'Student updated successfully'}, status=200)
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Student not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteStudentView(View):
    @method_decorator(require_POST)
    def post(self, request, id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return JsonResponse({'message': 'Student deleted successfully'}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('portal:login')  # Use namespace

def health_check(request):
    """
    A simple view to verify the application is working
    """
    return HttpResponse("OK", content_type="text/plain")

def debug_info(request):
    """
    A view that returns debug information about the environment
    """
    info = [
        f"Python version: {sys.version}",
        f"Django version: {django.get_version()}",
        f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}",
        f"DEBUG: {settings.DEBUG}",
        f"Request META: {request.META.get('HTTP_HOST', 'unknown')}",
        f"Request path: {request.path}",
        f"Request method: {request.method}",
        f"Request is secure: {request.is_secure()}",
        f"Request headers: {dict(request.headers)}",
    ]
    return HttpResponse("<br>".join(info), content_type="text/html")
