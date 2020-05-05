
from main.models import Student, Employer, Achivement, View, Vacancy
from rest_framework import viewsets
from api.serializers import StudentSerializer, EmployerSerializer, AchivementSerializer, ViewSerializer, VacancySerializer
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

@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def students(request):    
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True, context={'request': request})        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if len(Student.objects.filter(username=serializer.data["username"])) > 0:
                return Response({"error": "Такой пользователь уже существует!"})
            serializer.save()
            student = Auth_User.objects.create_user(username=serializer.data['username'], password=serializer.data['password'])
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def student_create(request):    
    serializer = StudentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def student_change(request):    
    serializer = StudentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):    
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    



@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def student_detail_name(request, username):        
    try:
        student = Student.objects.filter(username=username).first()
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)            

    if request.method == 'GET':
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        data = request.POST
        if data.get("login"):
            student.login = data.get("login")
        if data.get("password"):
            student.password = data.get("password")
        if data.get("name"):
            student.name = data.get("name")
        if data.get("image"):
            student.image = data.get("image")
        student.save()
        serializer = StudentSerializer(student, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_achivements(request, pk):    
    if request.method == 'GET':
        student = Student.objects.filter(id=pk).first()
        achivements = student.achivements
        serializer = AchivementSerializer(achivements, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achivements(request):    
    if request.method == 'GET':
        achivements = Achivement.objects.all()
        serializer = AchivementSerializer(achivements, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_views(request, pk):    
    if request.method == 'GET':
        student = Student.objects.filter(id=pk).first()
        views = student.views
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employer_vacancies(request, pk):    
    if request.method == 'GET':
        employer = Employer.objects.filter(id=pk).first()
        vacancies = Vacancy.objects.filter(owner=employer)
        serializer = VacancySerializer(vacancies, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vacancies(request):    
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        serializer = VacancySerializer(vacancies, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vacancy_id(request, pk):    
    if request.method == 'GET':
        vacancy = Vacancy.objects.filter(id=pk).first()
        serializer = VacancySerializer(vacancy, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vacancy_views(request, pk):    
    if request.method == 'GET':
        vacancy = Vacancy.objects.filter(id=pk).first()
        views = vacancy.views
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def employers(request):    
    if request.method == 'GET':
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True, context={'request': request})        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if len(Employer.objects.filter(username=serializer.data["username"])) > 0:
                return Response({"error": "Такой пользователь уже существует!"})
            serializer.save()
            student = Auth_User.objects.create_user(username=serializer.data['username'], password=serializer.data['password'])
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def employer_change(request):    
    serializer = EmployerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employer_detail(request, pk):    
    try:
        employer = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployerSerializer(employer, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployerSerializer(employer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    



@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def employer_detail_name(request, username):        
    try:
        employer = Employer.objects.filter(username=username).first()
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)            

    if request.method == 'GET':
        serializer = EmployerSerializer(employer, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployerSerializer(employer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        data = request.POST
        if data.get("login"):
            employer.login = data.get("login")
        if data.get("password"):
            employer.password = data.get("password")
        if data.get("name"):
            employer.name = data.get("name")
        if data.get("image"):
            employer.image = data.get("image")
        employer.save()
        serializer = EmployerSerializer(employer, context={'request': request})
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def achivement_detail(request, pk):    
    try:
        achivement = Achivement.objects.get(pk=pk)
    except Achivement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
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
