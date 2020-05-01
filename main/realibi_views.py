from django.shortcuts import render
from .models import Employer, Request
from .views import get_current_user
from django.http import HttpResponse

def employer_profile(request):
    user = get_current_user(request)
    print("[INFO] User id: " + str(user.id))

    return render(request, 'employer_profile.html', {
        "user": user
    })


def send_request(request):
    student_id = request.POST['student_id']
    user = get_current_user(request)
    new_request = Request.objects.create(owner=user)

    new_request.save()


    return render(request, 'message.html', { "text": "Приглашение отправлено успешно!" })