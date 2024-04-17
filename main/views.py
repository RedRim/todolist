from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import List, Task, Invitation
from .forms import AddTaskForm, AddListForm, InviteUserForm


@login_required
def lists_view(request):
    lists = List.objects.filter(participants=request.user)
    form = AddListForm()

    context = {
        'lists': lists,
        'title': 'Списки дел',
        'form': form,
    }
    return render(request, 'main/index.html', context)


@login_required
def add_list(request):
    if request.method == 'POST':
        form = AddListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.save()
            new_list.participants.add(request.user)
            return redirect('index')
    else:
        form = AddListForm()
    return render(request, 'main/index.html', {'form': form})


def delete_list(request, list_id):
    list = get_object_or_404(List, id=list_id)
    list.participants.remove(request.user)
    return redirect('index')


@login_required
def tasks_view(request, list_id):
    list = get_object_or_404(List, id=list_id)
    tasks = list.tasks.all()
    add_form = AddTaskForm()
    invite_form = InviteUserForm()
    participants = list.participants

    context = {
        'tasks': tasks,
        'list': list,
        'add_form': add_form,
        'invite_form': invite_form,
        'participants': participants,
    }
    return render(request, 'main/tasks.html', context)


@login_required
def add_task(request, list_id):
    list = get_object_or_404(List, id=list_id)

    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.list = list
            new_task.save()
            return redirect('tasks', list_id=list_id)
    else:
        form = AddTaskForm()

    context = {
        'list': list,
        'add_form': form,
    }

    return render(request, 'main/tasks.html', context)


@login_required
def delete_task(request, task_id):
    del_task = get_object_or_404(Task, id=task_id)
    list_id = del_task.list.id
    del_task.delete()
    return redirect('tasks', list_id=list_id)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True

    task.save()

    list_id = task.list.id
    list = get_object_or_404(List, id=list_id)
    if list.is_list_completed():
        list.is_completed = True

    return redirect('tasks', list_id=list_id)


def invite_user(request, list_id):
    list = get_object_or_404(List, id=list_id)

    if request.method == 'POST':
        form = InviteUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                invited_user = User.objects.get(username=username)
                Invitation.objects.create(
                    user_from=request.user, user_to=invited_user, list=list)
                return redirect('tasks', list_id=list.id)
            except User.DoesNotExist:
                pass
    else:
        form = InviteUserForm()

    context = {
        'list': list,
        'invite_form': form,
    }
    return render(request, 'main/tasks.html', context=context)


def user_invitations(request):
    invitations = Invitation.objects.filter(
        user_to=request.user).filter(status=Invitation.Status.WAITING)

    context = {
        'invitations': invitations
    }
    if not invitations.exists():
        context['no_invitations'] = True
    return render(request, 'main/invitations.html', context=context)


def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    invitation.status = Invitation.Status.ACCEPTED
    invitation.save()
    list = invitation.list
    list.participants.add(invitation.user_to)

    return redirect('tasks', list_id=list.id)


def reject_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id)
    invitation.status = Invitation.Status.REJECTED
    invitation.save()

    return redirect('user_invitations')
