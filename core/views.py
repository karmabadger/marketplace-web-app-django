from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, EmailForm #, mySetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, password_reset_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.db import IntegrityError
import requests
import json

# Create your views here.

global_user = {}

# def signup(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#             except IntegrityError:
#                 form.add_error('username', 'username is taken')
#     return render(request, 'registration/signup.html', { 'form': form })

def signup(request):
    if request.method == 'POST':
        context = {}
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            mysend_email(email)
            # email.send()
            return render(request, 'registration/waitactivation.html', context)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def myaccount(request):
    context = {'username': request.user.username}
    return render(request, 'registration/account/myaccount.html', context)

def activate(request, uidb64, token):
    context = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/waitactivation.html', context)
    else:
        return render(request, 'registration/linkError.html', context)
    
def reset_form(request):
    context = {}
    return render(request, 'registration/resetform.html', context)
    
def reset_request(request):
    if request.method == 'POST':
        context = {}
        form = EmailForm(request.POST)
        useremail = request.POST.get("email")
        print(useremail)
        user1 = User.objects.filter(email=useremail)[0]
        global global_user
        global_user = user1
        
        current_site = get_current_site(request)
        mail_subject = 'Reset Your Password'
        token = password_reset_token.make_token(user1)
        print("token is : ", token)
        message = render_to_string('registration/reset_email.html', {
            'user': user1,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user1.pk)),
            'token': token,
        })
        to_email = useremail
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        mysend_email(email)
        return render(request, 'registration/waitreset.html', context)
    
    else:
        form = EmailForm()
        return render(request, 'registration/resetform.html', {'form': form})
    
def resetpass(request, uidb64, token):
    context = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        global global_user
        global_user = user
        
        print("global user is " + str(global_user.password))
        print("now token is: ", token)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("error")
    if user is not None and password_reset_token.check_token(user, token):
        form = SetPasswordForm(user)
        return render(request, 'registration/resetpass.html', {'form': form, 'user': user})
    else:
        return render(request, 'registration/linkError.html', context)
    
def resetconfirmed(request):
    context = {}
    form = SetPasswordForm(request.POST)
    global global_user
    # print("global user is " + str(global_user.password))
    password = request.POST.get("new_password1")
    hashed_password = make_password(password)
    # print("unhashed password is: ", password)
    # print("Hashed password is: ", hashed_password)
    
    global_user.password = hashed_password
    global_user.save()
    return render(request, 'registration/resetconfirmed.html', context)


def get_validate(email):
    return requests.get(
        "https://api.mailgun.net/v4/address/validate",
        auth=("api", "f2a36cb54ee3e4953af6c97b38dd6cab-915161b7-6458b7be"),
        params={"address": email})

def mail_res_to_dic(res):
    return json.loads(res.text)

def mysend_email(email):
    res = requests.post(
            "https://api.mailgun.net/v3/testmp.stix.site/messages",
            auth=("api", "f2a36cb54ee3e4953af6c97b38dd6cab-915161b7-6458b7be"),
            params={"address": email.from_email},
            data={
                "subject": email.subject,
                "from": "wenxuan27@outlook.com",
                "to": email.to,
                "text": email.body,
                "html": email.body
            })
    
    print(res.text)
    print(email.from_email)
    return res
