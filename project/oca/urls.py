from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),

    #oca dashboard

    path('club_detail/<int:club_id>/', views.club_detail, name='club_detail'),
    path('approve_event/<int:event_id>/', views.approve_event, name='approve_event'),
    

    path('messaging/', views.messaging, name='messaging'),  # For clubs to message OCA
    path('messaging/<int:club_id>/', views.messaging, name='messaging_club'),  # For OCA to message clubs
    # club dashboard urlsf
    path('room_booking/', views.room_booking, name='room_booking'),
    path('room_booking_form/', views.room_booking_form, name='room_booking_form'),
    path('event_management/', views.event_management, name='event_management'),
    path('event_management/add/', views.add_event, name='add_event'),
    path('budget_form/', views.budget_form, name='budget_form'),
    path('budget_management/', views.budget_management, name='budget_management'),
    path('approve_budget/<int:budget_id>/', views.approve_event, name='approve_budget'),

    
]
