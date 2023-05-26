from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TodoForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.utils import timezone


# Create your views here.
def home(request):
    if User.objects.filter(username=request.user):
        return redirect('current')
    return render(request, 'todo/home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    elif request.method == 'POST':
        if not request.POST['password1'] == request.POST['password2']:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Вы ввели пароль который не совпадает!'})
        try:
            user = User.objects.create_user(
                request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('current')
        except IntegrityError:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Такой пользователь уже существует, попробуйте создать другого'})


@login_required
def logoutuser(request):
    logout(request)
    return redirect('home')

def auth_account(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        if not request.POST['username'] or not request.POST['password']:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Вы не ввели логин или пароль.'})
        
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Вы успешно авторизовались.')
            return redirect('current')
        else:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Вы ввели неверный логин или пароль.'})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'todo/create_task.html', {'form': TodoForm})
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new = form.save(commit=False)
            new.user_id = request.user
            new.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/create_task.html', {'form': TodoForm, 'error': 'Переданы неправильные данные.'})

@login_required
def current(request):
    todo = Todo.objects.filter(user_id=request.user, endtime__isnull=True)
    return render(request, 'todo/current.html', {'todos': todo})

@login_required
def finished_tasks(request):
    todo = Todo.objects.filter(user_id=request.user, endtime__isnull=False)
    return render(request, 'todo/current.html', {'todos': todo})


@login_required
def view_task(request, task_pk):
    task = get_object_or_404(Todo, pk=task_pk, user_id=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=task)
        return render(request, 'todo/view_task.html', {'todos': task, 'form': form})
    elif request.method == 'POST':
        if request.POST.get('button') == 'complete':
            return complete_task(request, task_pk)
        elif request.POST.get('button') == 'delete':
            return delete_task(request, task_pk)
        try:
            form = TodoForm(request.POST, instance=task)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/view_task.html', {'todos': task, 'form': form, 'error': 'Переданы неправильные данные.'})


@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(Todo, pk=task_pk, user_id=request.user)
    if request.method == 'POST':
        task.endtime = timezone.now()
        task.save()
        return redirect('current')
    
@login_required    
def delete_task(request, task_pk):
    task = get_object_or_404(Todo, pk=task_pk, user_id=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('current')