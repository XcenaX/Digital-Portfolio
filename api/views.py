
from main.models import Student#, Chat, Message
from rest_framework import viewsets
from api.serializers import StudentSerializer, EmployerSerializer, AchivementSerializer, ViewSerializer
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
#@permission_classes([IsAuthenticated])
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
#@permission_classes([IsAuthenticated])
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

@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def student_achivements(request, pk):    
    if request.method == 'GET':
        student = Student.objects.filter(id=pk).first()
        achivements = student.achivements
        serializer = AchivementSerializer(achivements, many=True, context={'request': request})        
        return Response(serializer.data)

@api_view(['GET', "POST"])
@permission_classes([IsAuthenticated])
def student_views(request, pk):    
    if request.method == 'GET':
        student = Student.objects.filter(id=pk).first()
        views = student.views
        serializer = ViewSerializer(views, many=True, context={'request': request})        
        return Response(serializer.data)


@api_view(['POST'])
def token(request):
    data = {
        "token": secrets.token_hex(20)
    }
    return Response(data)
