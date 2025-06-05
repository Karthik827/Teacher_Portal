from django.urls import path
from .views import (
    RegisterView, LoginView, HomeView, StudentListView, 
    AddStudentView, UpdateStudentView, DeleteStudentView, 
    LogoutView, health_check, #debug_info
)

app_name = 'portal'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('students/', StudentListView.as_view(), name='get_students'),
    path('student/', AddStudentView.as_view(), name='add_student'),
    path('student/<int:id>/', UpdateStudentView.as_view(), name='update_student'),
    path('student/<int:id>/delete/', DeleteStudentView.as_view(), name='delete_student'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('health/', health_check, name='health_check'),
    # path('debug/', debug_info, name='debug_info'),
]
