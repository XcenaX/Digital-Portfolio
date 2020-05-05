from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('students/', views.students, name="students"),    
    path('students/<int:pk>', views.student_detail, name="student-id"),
    path('students/<slug:username>', views.student_detail_name, name="student-name"),
    path('students/<int:pk>/achivements', views.student_achivements, name="student-achivements"),
    path('students/<int:pk>/views', views.student_views, name="student-views"),

    path('employers/', views.employers),    
    path('employers/<int:pk>', views.employer_detail, name="employer-id"),
    path('employers/<slug:username>', views.employer_detail_name, name="employer-name"),
    path('employers/<int:pk>/vacancies', views.employer_vacancies, name="employer-vacancies"),

    path('vacancies/', views.vacancies, name="vacancies"),
    path('vacancies/<int:pk>', views.vacancy_id, name="vacancy-id"),
    path('vacancies/<int:pk>/views', views.vacancy_views, name="vacancy-views"),  

    path('achivements', views.achivements, name="achivements"),
    path('achivements/<int:pk>', views.achivement_detail),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    
]

urlpatterns = format_suffix_patterns(urlpatterns)



    