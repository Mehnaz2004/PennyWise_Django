from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DetailView, TemplateView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser
from django.conf import settings
from django.views import View

def base(request):
    username = request.user.username
    # Pass the username to the context
    return render(request, 'registration/base.html', {'username': username})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('expense_sheet_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)  # Redirect to LOGIN_REDIRECT_URL after login
    return render(request, 'register/login.html')

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'registration/logout.html')
    
    def post(self, request):
        logout(request)
        return redirect('home')  # Redirect to your desired page after logout

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'registration/profile_view.html'

    def get_object(self):
        return self.request.user
    

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/delete_account.html'

    def post(self, request, *args, **kwargs):
        CustomUser = request.user
        CustomUser.delete_account()
        return redirect('login')