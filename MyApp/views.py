from django.contrib.sites.shortcuts import get_current_site

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes


from .forms import SignUpForm
from .models import account_activation_token



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # print('Form is valid')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.save()


            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Registered Successfully for  ' + user.username + '!' + 'Please click the link in your email to activate your account')
            return redirect('login')

        else:

            return render(request, 'registration/login.html', {'form': form})


    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        # if not user.password:
        return render(request, 'set_new_password.html', {'token': token, 'uidb64': uidb64})
        # login(request, user)
        # return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def set_new_password(request):
    data = request.POST
    try:
        uid = force_text(urlsafe_base64_decode(data['uidb64']))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.set_password(data['password1'])
        user.save()
        login(request, user)
    messages.success(request, 'All Set Password updated successfully')
    return redirect('home')

