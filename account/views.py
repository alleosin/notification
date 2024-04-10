from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, NotificationSendForm
from .models import Profile, Notification
from django.contrib import messages

@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profil paśpiachova abnoŭleny")
        else:
            messages.error(request, "Pamyłka ŭ abnaŭleńni profilu")
        return render(request, "account/dashboard.html", {"section": "dashboard"})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, "account/edit.html", {"user_form": user_form, "profile_form": profile_form})

def user_page(request, username):
    owner = get_object_or_404(Profile, user=username)
    if request.user == owner.user:
        notifications = Notification.objects.filter(addressee = owner).order_by("-created_date")
        context = {
            "owner": owner,
            "notifications": notifications,
        }
        return render(request, "account/user_page.html", context)
    elif request.method == "POST":
        notification_form = NotificationSendForm(data=request.POST)
        if notification_form.is_valid():
            new_notification = notification_form.save(commit=False)
            if new_notification.sender == "":
                new_notification.sender = "Ananim"
            new_notification.addressee = owner
            new_notification.save()
    else:
        notification_form = NotificationSendForm()
    return render(request, "account/notification.html", {"owner": owner, "notification_form": notification_form,})
