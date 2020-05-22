
from main.models import Student, Employer, Achivement, View, Vacancy, VacancyView
from rest_framework import viewsets
from api.serializers import StudentSerializer, EmployerSerializer, AchivementSerializer, ViewSerializer, VacancySerializer, VacancyViewSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as Auth_User
import secrets


#  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def students(request):    
    if request.method == 'POST':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):    
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data) 



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_detail_name(request, username):        
    try:
        student = Student.objects.filter(username=username).first()
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)            

    if request.method == 'POST':
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data)

  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_achivements(request, pk):    
    if request.method == 'POST':
        student = Student.objects.filter(id=pk).first()
        achivements = student.achivements
        serializer = AchivementSerializer(achivements, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def achivements(request):    
    if request.method == 'POST':
        achivements = Achivement.objects.all()
        serializer = AchivementSerializer(achivements, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_views(request, pk):    
    if request.method == 'POST':
        student = Student.objects.filter(id=pk).first()
        views = student.views
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employer_vacancies(request, pk):    
    if request.method == 'POST':
        employer = Employer.objects.filter(id=pk).first()
        vacancies = Vacancy.objects.filter(owner=employer)
        serializer = VacancySerializer(vacancies, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vacancies(request):    
    if request.method == 'POST':
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vacancy_id(request, pk):    
    if request.method == 'POST':
        vacancy = Vacancy.objects.filter(id=pk).first()
        serializer = VacancySerializer(vacancy, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def views(request):    
    if request.method == 'POST':
        views = View.objects.all()
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_id(request, pk):    
    if request.method == 'POST':
        view = View.objects.filter(id=pk).first()
        serializer = ViewSerializer(view, many=False, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vacancy_views(request):    
    if request.method == 'POST':
        vacancyview = VacancyView.objects.all()
        serializer = VacancyViewSerializer(vacancyview, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vacancy_view_id(request, pk):    
    if request.method == 'POST':
        vacancyview = VacancyView.objects.filter(id=pk).first()
        serializer = VacancyViewSerializer(vacancyview, many=False, context={'request': request})        
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vacancy_views(request, pk):    
    if request.method == 'POST':
        vacancy = Vacancy.objects.filter(id=pk).first()
        views = vacancy.views
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employers(request):    
    if request.method == 'POST':
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employer_detail(request, pk):    
    try:
        employer = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = EmployerSerializer(employer, context={'request': request})
        return Response(serializer.data)  



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def employer_detail_name(request, username):        
    try:
        employer = Employer.objects.filter(username=username).first()
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)            

    if request.method == 'POST':
        serializer = EmployerSerializer(employer, context={'request': request})
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def achivement_detail(request, pk):    
    try:
        achivement = Achivement.objects.get(pk=pk)
    except Achivement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = AchivementSerializer(achivement, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AchivementSerializer(achivement, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        achivement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


@api_view(['POST'])
def token(request):
    data = {
        "token": secrets.token_hex(20)
    }
    return Response(data)
