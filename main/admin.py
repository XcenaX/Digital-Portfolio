from django.contrib import admin
from .models import Student, Employer, Request,Achivement, View, Vacancy, Applied_Vacancy, VacancyView

admin.site.register(Student)
admin.site.register(VacancyView)
admin.site.register(Employer)
admin.site.register(Request)
admin.site.register(Achivement)
admin.site.register(View)
admin.site.register(Vacancy)
admin.site.register(Applied_Vacancy)