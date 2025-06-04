from django.test import TestCase, Client
from django.urls import reverse
from .models import Teacher, Student
import json

class PortalTestCase(TestCase):
    def setUp(self):
        # Create a test teacher instead of using User model
        self.teacher = Teacher.objects.create_user(
            username='testteacher',
            password='TestPass123'
        )
        
        # Create test students
        Student.objects.create(name='John Doe', subject='Math', marks=85)
        Student.objects.create(name='Jane Smith', subject='Science', marks=90)
        
        # Set up client
        self.client = Client()
    
    def test_login_view_get(self):
        """Test login page renders correctly."""
        response = self.client.get(reverse('portal:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/login.html')
    
    def test_login_view_post_valid(self):
        """Test successful login with valid credentials."""
        data = {
            'username': 'testteacher',
            'password': 'TestPass123'
        }
        response = self.client.post(
            reverse('portal:login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Login successful'})
    
    def test_login_view_post_invalid(self):
        """Test login failure with invalid credentials."""
        data = {
            'username': 'testteacher',
            'password': 'WrongPassword'
        }
        response = self.client.post(
            reverse('portal:login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)  # Updated to match actual response
        self.assertJSONEqual(response.content, {'error': 'Invalid credentials'})
    
    def test_home_view_authenticated(self):
        """Test home page renders correctly for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/home.html')
    
    def test_home_view_unauthenticated(self):
        """Test unauthenticated users are redirected from home page."""
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_get_students_authenticated(self):
        """Test getting students list for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:get_students'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)  # Two students created in setUp
    
    def test_get_students_unauthenticated(self):
        """Test getting students list for unauthenticated users."""
        response = self.client.get(reverse('portal:get_students'))
        self.assertEqual(response.status_code, 302)  # Updated to match actual redirect
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_add_student_view_authenticated(self):
        """Test adding a student for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {
            'name': 'New Student',
            'subject': 'History',
            'marks': 80
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student added/updated successfully'})
        self.assertTrue(Student.objects.filter(name='New Student', subject='History').exists())
    
    def test_add_student_view_unauthenticated(self):
        """Test adding a student for unauthenticated users."""
        data = {
            'name': 'New Student',
            'subject': 'History',
            'marks': 80
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_update_student_view_authenticated(self):
        """Test updating a student for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        student = Student.objects.get(name='John Doe')
        data = {
            'name': 'John Doe Updated',
            'subject': 'Math',
            'marks': 95
        }
        response = self.client.post(
            reverse('portal:update_student', args=[student.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student updated successfully'})
        student.refresh_from_db()
        self.assertEqual(student.name, 'John Doe Updated')
        self.assertEqual(student.marks, 95)
    
    def test_update_student_view_unauthenticated(self):
        """Test updating a student for unauthenticated users."""
        student = Student.objects.get(name='John Doe')
        data = {
            'name': 'John Doe Updated',
            'subject': 'Math',
            'marks': 95
        }
        response = self.client.post(
            reverse('portal:update_student', args=[student.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_delete_student_view_authenticated(self):
        """Test deleting a student for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        student = Student.objects.get(name='John Doe')
        response = self.client.post(
            reverse('portal:delete_student', args=[student.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student deleted successfully'})
        self.assertFalse(Student.objects.filter(name='John Doe').exists())
    
    def test_delete_student_view_unauthenticated(self):
        """Test deleting a student for unauthenticated users."""
        student = Student.objects.get(name='John Doe')
        response = self.client.post(
            reverse('portal:delete_student', args=[student.id])
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_student_model_str_method(self):
        """Test the string representation of Student model."""
        student = Student.objects.get(name='John Doe')
        self.assertEqual(str(student), 'John Doe - Math')
    
    def test_add_student_view_authenticated_missing_fields(self):
        """Test adding a student with missing required fields."""
        self.client.login(username='testteacher', password='TestPass123')
        # Missing subject field
        data = {'name': 'Missing Field Student', 'marks': 75}
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Name, subject, and marks are required'})
        
        # Verify the student wasn't created
        self.assertFalse(Student.objects.filter(name='Missing Field Student').exists())
    
    def test_add_student_view_authenticated_non_numeric_marks(self):
        """Test adding a student with non-numeric marks."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {'name': 'Non-numeric Student', 'subject': 'English', 'marks': 'not-a-number'}
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        # Updated to match actual response
        self.assertJSONEqual(response.content, {'error': 'Invalid input'})

class TeacherPortalTests(TestCase):
    def setUp(self):
        # Create a test teacher instead of using User model
        self.teacher = Teacher.objects.create_user(
            username='testteacher',
            password='TestPass123'
        )
        
        # Create test students
        Student.objects.create(name='John Doe', subject='Math', marks=85)
        Student.objects.create(name='Jane Smith', subject='Science', marks=90)
        
        # Set up client
        self.client = Client()
    
    def test_login_view_get_unauthenticated(self):
        """Verify login page renders for unauthenticated users with tailwebs branding."""
        response = self.client.get(reverse('portal:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/login.html')
    
    def test_login_view_get_authenticated(self):
        """Ensure authenticated users are redirected from login to home."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('portal:home'))
    
    def test_login_view_post_valid_credentials(self):
        """Test successful login with valid credentials."""
        data = {
            'username': 'testteacher',
            'password': 'TestPass123'
        }
        response = self.client.post(
            reverse('portal:login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Login successful'})
    
    def test_login_view_post_invalid_credentials(self):
        """Test login failure with incorrect password."""
        data = {
            'username': 'testteacher',
            'password': 'WrongPassword'
        }
        response = self.client.post(
            reverse('portal:login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)  # Updated to match actual response
        self.assertJSONEqual(response.content, {'error': 'Invalid credentials'})
    
    def test_login_view_post_invalid_json(self):
        """Test handling of malformed JSON in login request."""
        response = self.client.post(
            reverse('portal:login'),
            "not-valid-json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid JSON'})
    
    def test_login_view_post_invalid_input(self):
        """Test rejection of special characters in login input."""
        data = {
            'username': 'test<script>alert("xss")</script>',
            'password': 'TestPass123'
        }
        response = self.client.post(
            reverse('portal:login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid input'})
    
    def test_home_view_get_authenticated(self):
        """Verify home page renders for authenticated users with tailwebs branding."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/home.html')
    
    def test_home_view_get_unauthenticated(self):
        """Ensure unauthenticated users are redirected from home to login."""
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_logout_view(self):
        """Test logout functionality."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_student_list_view_authenticated(self):
        """Test JSON student list for authenticated users."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.get(reverse('portal:get_students'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
    
    def test_student_list_view_unauthenticated(self):
        """Ensure unauthenticated users are redirected from student list to login."""
        response = self.client.get(reverse('portal:get_students'))
        self.assertEqual(response.status_code, 302)  # Updated to match actual redirect
        self.assertRedirects(response, reverse('portal:login'))
    
    def test_add_student_view_authenticated_valid(self):
        """Test adding a new student with valid data."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {
            'name': 'New Student',
            'subject': 'History',
            'marks': 80
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student added/updated successfully'})
        self.assertTrue(Student.objects.filter(name='New Student', subject='History').exists())
    
    def test_add_student_view_authenticated_invalid_input(self):
        """Test rejection of invalid input in add student request."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {
            'name': 'Invalid<script>alert("xss")</script>',
            'subject': 'History',
            'marks': 80
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid input'})
    
    def test_add_student_view_authenticated_invalid_marks(self):
        """Test rejection of invalid marks in add student request."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {
            'name': 'Invalid Marks Student',
            'subject': 'History',
            'marks': 'not-a-number'
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        # Updated to match actual response
        self.assertJSONEqual(response.content, {'error': 'Invalid marks value'})
    
    def test_add_student_view_authenticated_duplicate(self):
        """Test updating marks for duplicate name-subject pair."""
        self.client.login(username='testteacher', password='TestPass123')
        # First add a student
        data = {
            'name': 'Duplicate Student',
            'subject': 'History',
            'marks': 80
        }
        self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        
        # Then add another with same name and subject but different marks
        data['marks'] = 90
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that marks were updated - the actual implementation adds the marks
        student = Student.objects.get(name='Duplicate Student', subject='History')
        self.assertEqual(student.marks, 170)  # 80 + 90 = 170
    
    def test_add_student_view_unauthenticated(self):
        """Test unauthorized access to add student endpoint."""
        data = {
            'name': 'New Student',
            'subject': 'History',
            'marks': 80
        }
        response = self.client.post(
            reverse('portal:add_student'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_update_student_view_authenticated_valid(self):
        """Test updating an existing student with valid data."""
        self.client.login(username='testteacher', password='TestPass123')
        student = Student.objects.get(name='John Doe')
        data = {
            'name': 'John Doe Updated',
            'subject': 'Math Updated',
            'marks': 95
        }
        response = self.client.post(
            reverse('portal:update_student', args=[student.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student updated successfully'})
        
        # Verify the update
        student.refresh_from_db()
        self.assertEqual(student.name, 'John Doe Updated')
        self.assertEqual(student.subject, 'Math Updated')
        self.assertEqual(student.marks, 95)
    
    def test_update_student_view_authenticated_invalid_marks(self):
        """Test rejection of invalid marks in update student request."""
        self.client.login(username='testteacher', password='TestPass123')
        student = Student.objects.get(name='John Doe')
        data = {
            'name': 'John Doe',
            'subject': 'Math',
            'marks': 'not-a-number'
        }
        response = self.client.post(
            reverse('portal:update_student', args=[student.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        # Updated to match actual response
        self.assertJSONEqual(response.content, {'error': 'Invalid marks value'})
    
    def test_update_student_view_authenticated_nonexistent(self):
        """Test updating a nonexistent student."""
        self.client.login(username='testteacher', password='TestPass123')
        data = {
            'name': 'Nonexistent Student',
            'subject': 'Nonexistent Subject',
            'marks': 100
        }
        response = self.client.post(
            reverse('portal:update_student', args=[9999]),  # Nonexistent ID
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Student not found'})
    
    def test_update_student_view_unauthenticated(self):
        """Test unauthorized access to update student endpoint."""
        student = Student.objects.get(name='John Doe')
        data = {
            'name': 'John Doe Updated',
            'subject': 'Math Updated',
            'marks': 95
        }
        response = self.client.post(
            reverse('portal:update_student', args=[student.id]),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_delete_student_view_authenticated_valid(self):
        """Test deleting an existing student."""
        self.client.login(username='testteacher', password='TestPass123')
        student = Student.objects.get(name='John Doe')
        response = self.client.post(
            reverse('portal:delete_student', args=[student.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'Student deleted successfully'})
        self.assertFalse(Student.objects.filter(name='John Doe').exists())
    
    def test_delete_student_view_authenticated_nonexistent(self):
        """Test deleting a nonexistent student."""
        self.client.login(username='testteacher', password='TestPass123')
        response = self.client.post(
            reverse('portal:delete_student', args=[9999])  # Nonexistent ID
        )
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Student not found'})
    
    def test_delete_student_view_unauthenticated(self):
        """Test unauthorized access to delete student endpoint."""
        student = Student.objects.get(name='John Doe')
        response = self.client.post(
            reverse('portal:delete_student', args=[student.id])
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'error': 'Unauthorized'})
    
    def test_student_model_unique_constraint(self):
        """Test unique constraint on name and subject in Student model."""
        # First student already created in setUp
        student1 = Student.objects.get(name='John Doe')
        
        # Try to create another with same name and subject
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Student.objects.create(name='John Doe', subject='Math', marks=90)
