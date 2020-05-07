from main.models import * 
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):    
    achivements = serializers.HyperlinkedRelatedField(many=True, view_name='achivement-id', read_only=True)
    views = serializers.HyperlinkedRelatedField(many=True, view_name='view-id', read_only=True)

    class Meta:
        model = Student
        fields = ["id", "is_searching_work", "email", "password", "username", "fullname", "img_url", "medcard_url", "university", "university_course", "specialty", "date_of_birth", "date_of_register", "is_active", "achivements", "views", "vk", "telegram", "about"]

class EmployerSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Employer
        fields = ["id", "email", "password", "username", "fullname", "img_url", "date_of_register", "is_active", "vk", "telegram", "description"]

class AchivementSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Achivement
        fields = ["id", "description", "img_url", "pub_date"]

class VacancySerializer(serializers.HyperlinkedModelSerializer):    
    owner = serializers.HyperlinkedRelatedField(many=False, view_name='employer-id', read_only=True)
    views = serializers.HyperlinkedRelatedField(many=True, view_name='view-id', read_only=True)

    class Meta:
        model = Vacancy
        fields = ["id", "title", "content", "pub_date", "salary", "is_active", "owner", "views"]

class ViewSerializer(serializers.HyperlinkedModelSerializer):    
    owner = serializers.HyperlinkedRelatedField(many=False, view_name='employer-id', read_only=True)
    class Meta:
        model = View
        fields = ["id", "owner"]

class VacancyViewSerializer(serializers.HyperlinkedModelSerializer):    
    owner = serializers.HyperlinkedRelatedField(many=False, view_name='student-id', read_only=True)
    class Meta:
        model = VacancyView
        fields = ["id", "owner"]
