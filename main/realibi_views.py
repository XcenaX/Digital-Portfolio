














from django.shortcuts import render
from .models import Employer
from .views import get_current_user

def employer_profile(request):
    user = get_current_user(request)
    print("[INFO] User id: " + str(user.id))

    return render(request, 'employer_profile.html', {
        "user": user
    })