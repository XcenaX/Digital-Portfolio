from main.models import * 
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):    
    achivements = serializers.HyperlinkedRelatedField(many=True, view_name='student-achivements', read_only=True)
    views = serializers.HyperlinkedRelatedField(many=True, view_name='student-views', read_only=True)

    class Meta:
        model = Student
        fields = ["is_searching_work", "email", "password", "username", "fullname", "img_url", "medcard_url", "university_course", "specialty", "date_of_birth", "date_of_register", "is_active", "achivements", "views", "vk", "telegram", "about"]

class EmployerSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Employer
        fields = ["email", "password", "username", "fullname", "img_url", "date_of_birth", "date_of_register", "is_active"]

class AchivementSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Achivement
        fields = ["description", "img_url", "pub_date"]

class ViewSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = View
        fields = ["owner"]
    
