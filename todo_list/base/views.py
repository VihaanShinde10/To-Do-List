from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}!')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    model = Task
    form_class = LoginForm
    template_name = 'base/login.html'
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class TaskList(LoginRequiredMixin,ListView):
    model = Task 
    template_name = 'base/task_list.html'
    context_object_name = 'tasklist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = Task.objects.filter(user=self.request.user)
        context['user'] = self.request.user
        return context
    
class TaskDetail(DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task'
    

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'description','complete']  # Add other fields you want to include in the form
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy('tasks')
    
class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    