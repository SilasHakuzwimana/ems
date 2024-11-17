from http.client import HTTPResponse
from django.urls import path # type: ignore

from event_management import settings
from . import views
from django.contrib.auth import views as auth_views  # type: ignore # noqa: F401

def debug_logout(request):
    return HTTPResponse("Logout was successful.")

urlpatterns = [
 path('', views.dashboard, name='dashboard'),  # Default route to dashboard

    path('events/', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
     path('event/new/', views.event_new, name='event_new'),  # URL to create new event
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # registration

     path('register/', views.register_view, name='register'),

    # user authentication and activities
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),  # Add `next_page`
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('accounts/profile/', views.profile, name='profile'), # Add this line
]