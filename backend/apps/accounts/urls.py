from django.urls import path
from .views import RegisterView, MeView, StaffUsersListView

urlpatterns = [
    path('register', RegisterView.as_view(), name='auth_register'),
    path('me', MeView.as_view(), name='auth_me'),
    # Endpoints staff
    path('staff/users', StaffUsersListView.as_view(), name='staff_users_list'),
]
