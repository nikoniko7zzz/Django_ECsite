from django.shortcuts import render
# from django import forms
# from django.http import request
# from django.shortcuts import render, redirect
# # from django.http import HttpResponse, request
# # from django.contrib.auth.views import LoginView
# # from blog.models import Article
# # from mysite.forms import ProfileForm, UserCreationForm
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
from django.core.mail import send_mail # gmail用
import os # gmail用



def contact(request):
    context = {}
    if request.method == "POST":
        # Gmail to me ---------
        subject = 'お問い合わせがありました(テスト用)'
        message = f'''
        お問い合わせがありました。\n
        名前: {request.POST.get('name')}\n
        メールアドレス: {request.POST.get('email')}\n
        内容: {request.POST.get('content')}
        '''
        email_from = os.environ['EMAIL_HOST_USER']
        email_to = [
            os.environ['EMAIL_HOST_USER'], # リストで複数入れることも可能
        ]
        send_mail(
                subject,
                message,
                email_from,
                email_to,
        )
        # Gmail ---------
        messages.success(request, 'メールを送信しました')

    return render(request, 'pages/contact.html', context)

