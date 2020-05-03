from django.shortcuts import render
from .models import Employer, Request, Student, Vacancy, Applied_Vacancy
from .views import get_current_user
from django.http import HttpResponse

def get_student_by_id(id):
    student = Student.objects.filter(id=id).first()

    if student:
        return student
    else:
        return False


def get_vacancy_by_id(id):
    vacancy = Vacancy.objects.filter(id=id).first()

    if vacancy:
        return vacancy
    else:
        return False


def employer_profile(request):
    user = get_current_user(request)
    print("[INFO] User id: " + str(user.id))

    return render(request, 'employer_profile.html', {
        "user": user
    })


def send_request(request):
    student_id = request.POST['student_id']
    student = get_student_by_id(student_id)

    user = get_current_user(request)
    new_request = Request.objects.create(owner=user, student=student)
    new_request.save()

    return render(request, 'message.html', { "text": "Приглашение отправлено успешно!" })


def get_vacancies_by_employer_id(id):
    vacancies = Vacancy.objects.filter(owner__id=id)
    return vacancies


def profile_add_vacancy(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        salary = request.POST['salary']
        user = get_current_user(request)

        vacancy = Vacancy.objects.create(title=title, content=content, salary=salary, owner=user)
        if vacancy.save():
            return render(request, 'profile_my_vacancies.html')

    return render(request, 'profile_add_vacancy.html')


def profile_my_vacancies(request):
    current_user = get_current_user(request)
    print("[INFO] --------------------- Current user id: " + str(current_user.id) + " -----------------")
    vacancies = get_vacancies_by_employer_id(current_user.id)
    return render(request, 'profile_my_vacancies.html', {"vacancies": vacancies})


def vacancy_show(request, id):
    vacancy = Vacancy.objects.filter(id=id).first()

    return render(request, 'vacancy_show.html', {
        'vacancy': vacancy
    }) 


def apply_vacancy(request):
    vacancy_id = request.POST['vacancy_id']
    current_user = get_current_user(request)
    vacancy = get_vacancy_by_id(vacancy_id)

    if Applied_Vacancy.objects.filter(vacancy=vacancy, student=current_user):
        return render(request, 'message.html', {'text': 'Вы уже откликались на вакансию ' + vacancy.title + '!'})
    else:
        applied_vacancy = Applied_Vacancy.objects.create(vacancy=vacancy, student=current_user)

        applied_vacancy.save()
        return render(request, 'message.html', {'text': 'Вы откликнулись на вакансию ' + vacancy.title + '!'})