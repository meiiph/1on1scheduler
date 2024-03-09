from django import forms
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.forms.models import model_to_dict
import json.decoder

class LogoutView(BaseLogoutView):
    next_page = '/accounts/login/' 

    def get_next_page(self):
        next_page = self.request.GET.get('next')
        if next_page:
            return resolve_url(next_page)
        return self.next_page

class ProfileView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            profile_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
            return JsonResponse(profile_data)
        else:
            return HttpResponse(status=401)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    password1 = forms.CharField(label="New password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1 and len(password1) < 8:
            raise ValidationError("This password is too short. It must contain at least 8 characters")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match")
        return password2 if password1 else None

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1 and self.user.is_authenticated:
            user.set_password(password1)
        if commit:
            user.save()
        return user
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('view_profile')
        else:
            # Serialize form errors to JSON
            errors = dict(form.errors.items())
            return JsonResponse(errors, status=400)
    else:
        form = EditProfileForm(instance=request.user, user=request.user)
        # Serialize form data to JSON
        form_data = model_to_dict(form.instance)
        return JsonResponse({'form_data': form_data})

class EditProfileView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = EditProfileForm(instance=request.user, user=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('view_profile')
        else:
            errors = dict(form.errors.items())
            return JsonResponse(errors, status=400)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered!")
            return redirect('login')  
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username or password is invalid'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_profile')
        else:
            error_message = "Username or password is invalid"
            messages.error(request, error_message)
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

@login_required
def view_profile(request):
    user = request.user
    profile_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(profile_data)
    else:
        return render(request, 'accounts/profile.html', {'profile_data': profile_data})

