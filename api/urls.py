from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('students/', views.students),    
    path('students/<int:pk>', views.student_detail),
    path('students/<slug:username>', views.student_detail_name),
    path('students/<int:pk>/achivements', views.student_achivements, name="student-achivements"),
    path('students/<int:pk>/views', views.student_views, name="student-views"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    
]

urlpatterns = format_suffix_patterns(urlpatterns)