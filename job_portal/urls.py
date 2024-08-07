from django.urls import path # type: ignore
from . import views
from .views import CountryChoicesAPIView, JobTitleChoicesAPIView, JobTypeChoicesAPIView, ExperienceChoicesAPIView, LocationChoicesAPIView, SectorChoicesAPIView, StatusChoicesAPIView, CategoryChoicesAPIView, CompanyListCreateView, CompanyDetailView, WorkplaceTypeChoicesAPIView

urlpatterns = [
    path('home', views.home, name='home'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job-type-choices/', JobTypeChoicesAPIView.as_view(), name='job_type_choices'),
    path('experience-choices/', ExperienceChoicesAPIView.as_view(), name='experience_choices'),
    path('category_choices/', CategoryChoicesAPIView.as_view(), name='category_choices'),
    path('workplace_choices/', WorkplaceTypeChoicesAPIView.as_view(), name='workplace_choices'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applications/<int:job_id>/', views.job_applications, name='job_applications'),
    path('status-choices/', StatusChoicesAPIView.as_view(), name='status_choices'),
    path('job-status/<int:job_id>/', views.job_status, name='job_status'),
    path('companies/', CompanyListCreateView.as_view(), name='company_list_create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('find_status/', views.find_status, name="find_status"),
    path('candidate_profile/', views.candidate_profile, name ="candidate_profile"),
    path('company_status/<str:status_choice>/', views.company_status, name= "company_status"),
    path('create/', views.create_resume, name='create_resume'),
    path('<int:pk>/', views.resume_detail, name='resume_detail'),
    path('sector_type_choices/', SectorChoicesAPIView.as_view(), name='sector_choices'),
    path('job_title_choices/', JobTitleChoicesAPIView.as_view(), name='job_title_choices'),
    path('country_type_choices/', CountryChoicesAPIView.as_view(), name='country_type_choices'),
    path('location_choices/', LocationChoicesAPIView.as_view(), name='location_choices'),
]
