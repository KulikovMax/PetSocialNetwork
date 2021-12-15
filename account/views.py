from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import User, Profile

from django.contrib.auth.decorators import login_required
from django.contrib import messages


def update_profile_lr(request):
    """
    Updates profile last request. Implemented in every view.
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        user.update_last_request()


@login_required
def dashboard(request):
    """
    Renders dashboard when user enters Account app section.
    :param request:
    :return: return render(request, 'account/edit.html', {'section': 'dashboard'})
    """
    user = User.objects.get(pk=request.user.pk)
    user.update_last_request()
    return render(request, 'account/edit.html', {'section': 'dashboard'})


def user_login(request):
    """
    Renders LoginForm, then authenticate user
    Checks User's LoginForm -> (Yes) Checks if User exists ->(Yse) Checks if activated -> (Yes) Logs In User
    If form is not valid recreates a form
    :param request:
    :return: render(request, 'account/login.html', {'form': form})
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user = User.objects.get(pk=request.user.pk)
                    user.update_last_login()
                    return redirect(reverse('dashboard'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    """
    Logout user
    :param request:
    :return: redirect(reverse('index'))
    """
    user = User.objects.get(pk=request.user.pk)
    user.update_last_request()
    if request.method == 'POST':
        logout(request)
        return redirect(reverse('index'))


def change_password(request):
    """
    Renders PasswordChangeForm
    Change password by user request after validating old password.
    :param request:
    :return: return render(request, 'account/change_password.html', {
        'form': form, 'user': request.user
    }) or redirect('change_password_done')
    """
    user = User.objects.get(pk=request.user.pk)
    user.update_last_request()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form, 'user': request.user
    })


def change_password_done(request):
    """
    Shows that password changed successfully
    :param request:
    :return: render(request, 'account/change_password_done.html')
    """
    user = User.objects.get(pk=request.user.pk)
    user.update_last_request()
    return render(request, 'account/change_password_done.html')


def sign_up(request):
    """
    Renders template with UserRegistrationForm, validating data and creating new User if valid
    :param request:
    :return: return render(request, 'account/sign_up.html', {'user_form': user_form}) or return render(request, 'account/sign_up_done.html', {'new_user': new_user})
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form['password'] != user_form['password_conf']:
            messages.error(request, "Your Passwords don't match")
            return redirect('sign_up')
        else:
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                profile = Profile.objects.create(user=new_user)
                return render(request, 'account/sign_up_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/sign_up.html', {'user_form': user_form})


@login_required
def edit(request):
    """
    Allows user to edit his profile info. Uses UserEditForm.
    :param request:
    :return: return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
    """
    user = User.objects.get(pk=request.user.pk)
    user.update_last_request()
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile edited successfully')
        else:
            messages.error(request, 'Something went wrong while updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
