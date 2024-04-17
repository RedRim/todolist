from django.urls import path

from .views import *

urlpatterns = [
    path('', lists_view, name='index'),
    path('tasks/<int:list_id>/', tasks_view, name='tasks'),
    path('add_task/<int:list_id>/', add_task, name='add_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),
    path('complete_task/<int:task_id>/', complete_task, name='complete_task'),
    path('add_list/', add_list, name='add_list'),
    path('invite_user/<int:list_id>/', invite_user, name='invite_user'),
    path('invitations/', user_invitations, name='user_invitations'),
    path('accept_invitation/<int:invitation_id>/', accept_invitation, name='accept_invitation'),
    path('reject_invitation/<int:invitation_id>/', reject_invitation, name='reject_invitation'),
    path('delete_list/<int:list_id>/', delete_list, name='delete_list'),
]