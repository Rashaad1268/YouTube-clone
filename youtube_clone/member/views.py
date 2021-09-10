from django.shortcuts import (render, redirect)
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Local imports
from base.models import CreatorProfile
from .forms import (CreateUserForm, EditProfileForm, PasswordChangingForm, CreatorProfileForm)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')
			

        context = {'form':form}
        return render(request, 'registration/register.html', context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            username = request.POST.get('username', None)
            password =request.POST.get('password', None)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

            elif not user:
                messages.info(request, "Username OR password is incorrect")

        # context = {"form":form}
        return render(request, 'registration/login.html', context)


@login_required(login_url='login')
def edit_profile(request):
    context = {}
    user_profile_form = EditProfileForm(instance=request.user)
    creator_profile_form = CreatorProfileForm(instance=request.user.creatorprofile)
    context["creator_profile_form"] = creator_profile_form

    if request.method == 'POST':
        user_profile_form = EditProfileForm(request.POST, instance=request.user)
        creator_profile_form = CreatorProfileForm(request.POST, request.FILES, instance=request.user.creatorprofile)

        # if :
            # user_profile_form.save()

        if creator_profile_form.is_valid() and user_profile_form.is_valid():
            user_profile = user_profile_form.save()
            creator_profile_form.creator = request.user
            creator_profile = creator_profile_form.save(commit=False)
            creator_profile.creator = user_profile
            creator_profile.save()
            # request.user.creatorprofile.save()
            messages.success(request, "Updated profile")
            return redirect("edit-profile")
	
    context["user_profile_form"] = user_profile_form
    return render(request, "registration/edit_profile.html", context)
