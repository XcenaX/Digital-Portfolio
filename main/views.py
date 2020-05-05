from django.shortcuts import render

#from .forms import UserForm, CommentForm, BlogForm
from .models import Student, Employer, Request, Achivement, Vacancy, View

from django.shortcuts import redirect
from django.urls import reverse

from .modules.hashutils import check_pw_hash, make_pw_hash

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

import smtplib, ssl

from .modules.sendEmail import send_email

from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

import os
from django.conf import settings
from django.http import HttpResponse, Http404

from django.db.models import Q

COUNT_BLOG_ON_PAGE=10


def get_paginated_blogs(request, paginator):
    page = request.GET.get('page')
    try:
        page = int(page)
    except:
        page = 1
    a = ""
    block = ""
    pages=[]
    if page:
        try:
            block = paginator.page(page)
        except EmptyPage:
            block = paginator.page(paginator.num_pages)
            page = paginator.num_pages

        for i in range(page-2, page+3):
            try:
                a = paginator.page(i)
                pages.append(i)
            except:
                continue
        print(pages)
        if pages[-1] != paginator.num_pages:
            pages.append(paginator.num_pages)

        if pages[0] != 1:
            pages.insert(0, 1)
    else:
        pages = [1,2,3,4,5,paginator.num_pages]
        block = paginator.page(1)
    return block, pages


def get_current_user(req):
    try:
        user = None
        user_id = req.session["user_id"]
        role = req.session["role"]
        print(role)
        if role == "student":
            user = Student.objects.filter(id=user_id).first()
        elif role == "employer":
            user = Employer.objects.filter(id=user_id).first()
        return user 
    except Exception as error:
        print(req.session)
        print(error)
        return None  

def get_parameter(request, name):
    try:
        return request.GET[name]
    except:
        return None 

def post_parameter(request, name):
    try:
        return request.POST[name]
    except:
        return None 

def post_file(request, name):
    try:
        return request.FILES[name]
    except:
        return None

def session_parameter(request, name):
    try:
        return request.session[name]
    except:
        return None

def filter_users(request):
    role = session_parameter(request, "role")
    q = get_parameter(request, "q")
    category = get_parameter(request, "category")
    
    if role == "student":
        if category == "old":
            blocks = Vacancy.objects.order_by("-pub_date")
        elif category == "new":
            blocks = Vacancy.objects.order_by("pub_date")
        elif category == "most_views":
            blocks = Vacancy.objects.order_by("-views")
        elif category == "few_views":
            blocks = Vacancy.objects.order_by("views")
        else:
            blocks = Vacancy.objects.all()
        if q:
            blocks = blocks.filter(Q(fullname__icontains=q) | Q(title__icontains=q) | Q(salary__icontains=q))
    #                                                                               это для того чтобы искать с условиями, типо содердится ли q там, там или там
    else:
        if category == "old":
            blocks = Student.objects.filter(is_searching_work=True).order_by("-date_of_register")
        elif category == "new":
            blocks = Student.objects.filter(is_searching_work=True).order_by("date_of_register")
        elif category == "most_views":
            blocks = Student.objects.filter(is_searching_work=True).order_by("-views")
        elif category == "few_views":
            blocks = Student.objects.filter(is_searching_work=True).order_by("views")
        else:
            blocks = Student.objects.filter(is_searching_work=True)
        if q:
            blocks = blocks.filter(Q(fullname__icontains=q) | Q(university__icontains=q) | Q(university_course__icontains=q) | Q(city__icontains=q))
    return blocks

def logout(request):
    if request.method == "POST":
        try:
            del request.session["user_id"]
            del request.session["role"]
        except:
            print("error")
    return redirect(reverse('main:index'))

def login(request):
    user = None
    if request.method == "POST":
        role = post_parameter(request, "role")
        email_or_username = post_parameter(request, "username")
        password = post_parameter(request, "pass")
        
        try:
            if role == "student":
                user = Student.objects.filter(email=email_or_username).first()
                if not user:
                    user = Student.objects.filter(username=email_or_username).first()
            elif role == "employer": 
                user = Employer.objects.filter(email=email_or_username).first()
                if not user:
                    user = Employer.objects.filter(username=email_or_username).first()
        except:
            user = None
        print(user)
        if user:
            if check_pw_hash(password, user.password):
                if not user.is_active:
                    return render(request, 'login.html', {
                        "login_error" : "Подтвердите свою почту чтобы войти!",
                    })
                request.session["user_id"] = user.id
                request.session["role"] = role
                return redirect(reverse('main:index'))
            else:
                return render(request, 'login.html', {
                    "login_error" : "Такого пользователя не существует!",
                })
        else:
            return render(request, 'login.html', {
                "login_error" : "Такого пользователя не существует!",
            })
    return render(request, 'login.html', {})

def register(request):
    user = True
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        username = request.POST['login']
        role = request.POST['role']
        
        if password != password_confirm:
            return render(request, 'register.html', {
                "register_error" : "Пароли не совпадают!",
            })

        if len(password) < 5:
            return render(request, 'register.html', {
                "register_error" : "Пароль должен быть не меньше 5 символов!",
            })

        try:
            if role == "student":
                students = Student.objects.filter(email=email)
                if len(students) > 0:
                    raise Exception
            elif role == "employer":
                employers = Employer.objects.filter(username=username)
                if len(employers) > 0:
                    raise Exception
        except:
           user = False
        
        if not user:
            return render(request, 'register.html', {
                "register_error" : "Такой пользователь уже существует!",
            })
        hash_password = make_pw_hash(password)
        current_user = None
        if role == "employer":
            current_user = Employer.objects.create(email=email, password=hash_password, username=username, fullname=fullname)
        elif role == "student":
            current_user = Student.objects.create(email=email, password=hash_password, username=username, fullname=fullname)
        
        current_user.save()
        

        try:
            current_site = get_current_site(request)
            mail_subject = 'Активируйте свой аккаунт!'
            message = render_to_string('acc_active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token':account_activation_token.make_token(current_user),
                "mail_subject": mail_subject,
            })
            to_email = current_user.email
            
            send_email(message, mail_subject, to_email)
            request.session["user_id"] = current_user.id
            request.session["role"] = role
            return render(request, 'message.html', {
                "text": "Вам на почту выслано письмо для подтверждения!"
            })
        except Exception as error:
            return render(request, 'message.html', {
                "text" : error,
            })
            
               
    return render(request, "register.html", {})


def activate(request, uidb64, token):
    user = None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Student.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Exception):
        user = None

    if not user:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Employer.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Exception):
            user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return redirect(reverse('main:index'))
        
    else:
        return render(request, 'message.html', {
                "text": "Неверная ссылка активации почты!"
            })
                

def index(request):
    q = get_parameter(request, "q")
    q = "" if not q else q
    category = get_parameter(request, "category")
    user = get_current_user(request)
    blocks = filter_users(request)

    paginator = Paginator(blocks, COUNT_BLOG_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)
    vacancies = Vacancy.objects.all()
    print('[INFO] Vacancies setted')

    if not user or not user.is_active:
        return redirect(reverse('main:login'))
        
    return render(request, 'index.html', {
        "user": user,
        "blocks": paginated_blocks,
        "pages": pages,
        "q": q,
        "category": category,
        "category_values": {
            "old": "Сначала старые", 
            "new": "Сначала новые", 
            "most_views": "Больше всего просмотров", 
            "fiew_views":"Меньше всего просмотров"
        },
        "vacancies": vacancies
    })

def not_found(request):
    user = get_current_user(request)
    return render(request, '404.html', {
        "user": user,
    })

def portfolio_edit(request):
    user = get_current_user(request)
    if request.session["role"] == "employer":
        return redirect(reverse('main:index'))
    if request.method == "POST":
        fullname = post_parameter(request, 'fullname')
        location = post_parameter(request, 'location')
        university = post_parameter(request, 'university')
        course = post_parameter(request, 'course')
        date_of_birth = post_parameter(request, 'date_of_birth')
        resume = post_parameter(request, 'resume')
        image = post_file(request, 'medcard')
        is_image = True
        try:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg"):
                upload_error = "Выберите .jpg или .png формат для медкарты!" 
                return render(request, 'portfolio_edit.html', {
                    "user": user,
                    "upload_error": upload_error,
                })
        except:
            is_image = False

        if is_image:
            new_img_url = '/home/digitalportfolio/Digital-Portfolio/main/static/images/user/medcards/medcard'+str(user.id)+'.jpg'
            with open(new_img_url, 'wb') as handler:
                for chunk in image.chunks():
                    handler.write(chunk)
            
            new_img_url = "/static/images/user/medcards/medcard" + str(user.id) + ".jpg"
            
            user.medcard_url = new_img_url
        user.fullname = fullname if fullname else user.fullname
        user.university_course = course if course else user.university_course
        user.date_of_birth = date_of_birth if date_of_birth else user.date_of_birth
        user.about = resume if resume else user.about
        user.university = university if university else user.university
        user.city = location if location else user.city

        user.save()

        
        return render(request, 'portfolio_edit.html', {
            "user": get_current_user(request),
            "success": "Вы успешно обновили профиль!"
        }) 

    
    return render(request, 'portfolio_edit.html', {
        "user": user,
    })    

def portfolio_show(request, id):
    employer = get_current_user(request)
    if employer:
        if request.session["role"] == "student":
            return render(request, 'after_register.html', {
                "text" : "Только работодатели могут просматривать портфолио студентов!",
            })
    user = Student.objects.filter(id=id).first()

    if len(user.views.filter(owner=employer)) == 0:
        view = View.objects.create(owner=employer)
        user.views.add(view)

    employer_request = Request.objects.filter(owner=employer).first()
    vacancies = Vacancy.objects.filter(owner=employer)
    
    is_request_sended = False
    if employer_request:
        is_request_sended = True

    return render(request, 'portfolio_show.html', {
        "student": user,
        "user": employer,
        "employer_request": employer_request,
        "is_request_sended": is_request_sended,
        "vacancies": vacancies
    }) 


def achivements_show(request, id):
    employer = get_current_user(request)
    if employer:
        if request.session["role"] == "student":
            return render(request, 'after_register.html', {
                "text" : "Только работодатели могут просматривать портфолио студентов!",
            })
    user = Student.objects.filter(id=id).first()
    employer_request = Request.objects.filter(owner=employer).first()
    is_request_sended = False
    if employer_request:
        is_request_sended = True

    achivements = user.achivements.all()
    paginator = Paginator(achivements, COUNT_BLOG_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)

    return render(request, 'portfolio_achivements_show.html', {
        "student": user,
        "user": employer,
        "employer_request": employer_request,
        "is_request_sended": is_request_sended,
        "blocks": paginated_blocks,
        "pages": pages,
    }) 

 

def portfolio_achivements(request):
    user = get_current_user(request)
    achivements = user.achivements.all()
    paginator = Paginator(achivements, COUNT_BLOG_ON_PAGE)
    paginated_blocks, pages = get_paginated_blogs(request, paginator)

    return render(request, 'portfolio_achivements.html', {
        "user": user,
        "blocks": paginated_blocks,
        "pages": pages,
    })   

def portfolio_requests(request):
    user = get_current_user(request)
    return render(request, 'portfolio_requests.html', {
        "user": user,
    })   

def portfolio_add_achivement(request):
    user = get_current_user(request)

    if request.method == "POST":
        description = post_parameter(request, 'description')
        image = post_file(request, 'achivement_img')

        try:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg"):
                upload_error = "Выберите .jpg или .png формат для картинки!" 
                return render(request, 'portfolio_add_achivement.html', {
                    "user": user,
                    "upload_error": upload_error,
                })
        except:
            upload_error = "Вы не выбрали картинку для сертификата!" 
            return render(request, 'portfolio_add_achivement.html', {
                "user": user,
                "upload_error": upload_error,
            })

        achivement = Achivement.objects.create(description=description)

        new_img_url = '/home/digitalportfolio/Digital-Portfolio/main/static/images/user/achivements/achivement'+str(achivement.id)+'.jpg'
        with open(new_img_url, 'wb') as handler:
            for chunk in image.chunks():
                handler.write(chunk)
        
        new_img_url = "/static/images/user/achivements/achivement" + str(achivement.id) + ".jpg"
        achivement.img_url = new_img_url
        achivement.save()
        user.achivements.add(achivement)
        user.save()
        return render(request, 'portfolio_add_achivement.html', {
            "user": user,
            "success": "Вы успешно добавили достижение!",
        })  


    return render(request, 'portfolio_add_achivement.html', {
        "user": user,
    })   

def delete_achivement(request):
    if request.method == "POST":
        achivement_id = post_parameter(request, "id")
        if achivement_id:
            Achivement.objects.get(id=achivement_id).delete()
    return redirect(reverse('main:portfolio_achivements'))

def update_avatar(request):
    role = session_parameter(request, "role")
    if request.method == "POST":
        user = get_current_user(request)
        if not user:
            if role == "student":
                return redirect(reverse('main:portfolio_edit'))
            else:
                return redirect(reverse('main:employer_profile'))
        image = post_file(request, 'avatar')
        print(image.name)
        try:
            if not image.name.endswith(".png") and not image.name.endswith(".jpg"):
                upload_error = "Выберите .jpg или .png формат для картинки!" 
                if role == "student":
                    return render(request, 'portfolio_edit.html', {
                        "user": user,
                        "upload_error": upload_error,
                    })
                else:
                    return render(request, 'employer_profile.html', {
                        "user": user,
                        "upload_error": upload_error,
                    })
        except:
            upload_error = "Вы не выбрали картинку для аватара!"
            if role == "student": 
                return render(request, 'portfolio_edit.html', {
                    "user": user,
                    "upload_error": upload_error,
                })
            else:
                return render(request, 'employer_profile.html', {
                    "user": user,
                    "upload_error": upload_error,
                })

        new_img_url = '/home/digitalportfolio/Digital-Portfolio/main/static/images/user/avatars/avatar'+str(user.id)+'.jpg'
        with open(new_img_url, 'wb') as handler:
            for chunk in image.chunks():
                handler.write(chunk)
        
        new_img_url = "/static/images/user/avatars/avatar" + str(user.id) + ".jpg"
        user.img_url = new_img_url
        user.save()

    if role == "student":
        return redirect(reverse('main:portfolio_edit'))
    else:
        return redirect(reverse('main:employer_profile'))


def update_social(request):
    if request.method == "POST":
        user = get_current_user(request)
        if not user:
            return redirect(reverse('main:portfolio_edit'))    
        telegram = post_parameter(request, 'telegram')
        vk = post_parameter(request, 'vk')
        user.vk = vk if vk else ""
        user.telegram = telegram if telegram else ""
        user.save()
    role = session_parameter(request, "role")
    if role == "student":
        return redirect(reverse('main:portfolio_edit'))
    else:
        return redirect(reverse('main:employer_profile'))

def switch_search(request):
    if request.method == "POST":
        user = get_current_user(request)
        is_search = post_parameter(request, 'is_search')
        user.is_searching_work = True if is_search == "on" else False
        user.save()
    return redirect(reverse('main:portfolio_edit') + "#is_search")


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404




