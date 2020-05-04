from django.shortcuts import render
from .models import Employer, Request, Student, Vacancy, Applied_Vacancy, VacancyView
from .views import get_current_user, get_current_site, render_to_string, send_email
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
    vacancy_id = request.POST['vacancy_id']

    vacancy = get_vacancy_by_id(vacancy_id)
    student = get_student_by_id(student_id)

    user = get_current_user(request)

    try:
        current_site = get_current_site(request)
        mail_subject = 'Приглашение на работу!'
        message = render_to_string('request_send_email.html', {
            'student': student,
            'vacancy': vacancy,
            "mail_subject": mail_subject,
        })
        to_email = student.email
        
        send_email(message, mail_subject, to_email)

    except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })
    

    new_request = Request.objects.create(owner=user, student=student, vacancy=vacancy, is_invitation=True)
    new_request.save()

    return render(request, 'message.html', { "text": "Приглашение отправлено успешно!" })


def get_vacancies_by_employer_id(id):
    vacancies = Vacancy.objects.filter(owner__id=id)
    return vacancies


def profile_add_vacancy(request):
    current_user = get_current_user(request)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        salary = request.POST['salary']
        user = get_current_user(request)

        vacancy = Vacancy.objects.create(title=title, content=content, salary=salary, owner=user)
        if vacancy.save():
            return render(request, 'profile_my_vacancies.html')

    return render(request, 'profile_add_vacancy.html',{
        "user": current_user
    })


def profile_delete_vacancy(request):
    if request.method == "POST":
        vacancy_id = request.POST['vacancyId']
        print('[INFO]----------------Vacancy id: ' + vacancy_id + '----------------')
        print("privet")
        vacancy = get_vacancy_by_id(vacancy_id)

        vacancy.delete()

    current_user = get_current_user(request)

    vacancies = get_vacancies_by_employer_id(current_user.id)
    return render(request, 'profile_my_vacancies.html', {
        "vacancies": vacancies,
        "user": current_user,
    })


def profile_my_vacancies(request):
    current_user = get_current_user(request)
    print("[INFO] --------------------- Current user id: " + str(current_user.id) + " -----------------")
    vacancies = get_vacancies_by_employer_id(current_user.id)
    return render(request, 'profile_my_vacancies.html', {
        "vacancies": vacancies,
        "user": current_user
    })


def vacancy_show(request, id):
    vacancy = Vacancy.objects.filter(id=id).first()
    current_user = get_current_user(request)

    if isinstance(current_user, Student):
        if len(VacancyView.objects.filter(owner=current_user)) == 0:
            view = VacancyView.objects.create(owner=current_user)
            vacancy.views.add(view)
            vacancy.save()

    requests = Request.objects.filter(vacancy=vacancy, is_applied=False, is_invitation=False)

    return render(request, 'vacancy_show.html', {
        'vacancy': vacancy,
        'requests': requests,
        "user": current_user
    }) 


def apply_vacancy(request):
    vacancy_id = request.POST['vacancy_id']
    current_user = get_current_user(request)
    vacancy = get_vacancy_by_id(vacancy_id)

    applied_vacancy = Applied_Vacancy.objects.filter(vacancy=vacancy, student=current_user).first()

    if applied_vacancy:
        if applied_vacancy.accepted:
            return render(request, 'message.html', {'text': 'Вы уже приглашены на эту вакансию!'})
        else:
            return render(request, 'message.html', {'text': 'К сожалению, работодатель уже отклонил ваше предложение по этой вакансии!'})
    else:
        vacancy_request = Request.objects.create(owner=vacancy.owner, student=current_user, vacancy=vacancy)

        vacancy_request.save()
        return render(request, 'message.html', {'text': 'Вы откликнулись на вакансию ' + vacancy.title + '! Ожидайте ответа от работодателя!'})


def accept_student(request):
    vacancy_id = request.POST['vacancy_id']
    student_id = request.POST['student_id']

    current_user = get_current_user(request)
    vacancy = Vacancy.objects.filter(id=vacancy_id).first()
    student = Student.objects.filter(id=student_id).first()

    vacancy_request = Request.objects.filter(student=student, vacancy=vacancy).first()
    vacancy_request.is_applied = True
    vacancy_request.save()

    applied_vacancy = Applied_Vacancy.objects.create(vacancy=vacancy, student=student, accepted=True)
    applied_vacancy.save()

    try:
        mail_subject = 'Приглашение на работу!'
        message = render_to_string('student_accepted_email.html', {
            'user': student,
            'vacancy': vacancy,
            "mail_subject": mail_subject,
        })
        to_email = student.email
        
        send_email(message, mail_subject, to_email)

    except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })

    return vacancy_show(request, vacancy_id)


def decline_student(request):
    vacancy_id = request.POST['vacancy_id']
    student_id = request.POST['student_id']

    vacancy = Vacancy.objects.filter(id=vacancy_id).first()
    student = Student.objects.filter(id=student_id).first()

    vacancy_request = Request.objects.filter(student=student, vacancy=vacancy)
    vacancy_request.delete()

    applied_vacancy = Applied_Vacancy.objects.create(vacancy=vacancy, student=student, accepted=False)
    applied_vacancy.save()

    try:
        mail_subject = 'В следующий раз повезет!'
        message = render_to_string('student_declined_email.html', {
            'user': student,
            'vacancy': vacancy,
            "mail_subject": mail_subject,
        })
        to_email = student.email
        
        send_email(message, mail_subject, to_email)

    except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })

    return vacancy_show(request, vacancy_id)