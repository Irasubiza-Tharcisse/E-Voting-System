from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # VOTER INTERFACE
    # ==========================================
    path('', views.election_list, name='election_list'),
    path('vote/<int:election_id>/', views.vote_view, name='vote'),
    path('results/<int:election_id>/', views.results_view, name='results'),

    # ==========================================
    # ADMIN DASHBOARD & CORE MANAGEMENT
    # ==========================================
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Election Actions
    path('admin/election/create/', views.election_create, name='election_create'),
    path('admin/election/edit/<int:pk>/', views.election_update, name='election_update'),
    path('admin/election/delete/<int:pk>/', views.election_delete, name='election_delete'),

    # ==========================================
    # POSITION MANAGEMENT
    # ==========================================
    path('admin/election/<int:election_id>/positions/', views.position_manage, name='position_manage'),
    path('admin/position/create/<int:election_id>/', views.position_create, name='position_create'),
    path('admin/position/edit/<int:pk>/', views.position_edit, name='position_edit'),
    # Add these to allow the "X" delete button on your dashboard badges
    path('admin/position/delete/<int:pk>/', views.position_delete, name='position_delete'),
    # ==========================================
    # CANDIDATE MANAGEMENT (With Profile Pics)
    # ==========================================
    # Step 1: Select which position the candidate belongs to
    path('admin/candidate/select/<int:election_id>/', views.candidate_create_selector, name='candidate_create_selector'),
    
    # Step 2: Fill in candidate details (Name, Bio, Profile Pic)
    path('admin/candidate/create/<int:position_id>/', views.candidate_create, name='candidate_create'),
    path('admin/election/<int:election_id>/candidates/', views.candidate_manage, name='candidate_manage'),
    
    # Candidate Actions
    path('admin/candidate/edit/<int:pk>/', views.candidate_edit, name='candidate_edit'),
    path('admin/candidate/delete/<int:pk>/', views.candidate_delete, name='candidate_delete'),
]