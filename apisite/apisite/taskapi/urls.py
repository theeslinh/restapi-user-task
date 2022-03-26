from django.contrib import admin
from django.urls import path, include
from . import jsonviews as views

app_name = 'taskapi'

urlpatterns = [
    path('index', views.index, name='App index'),
    #d signup
    path('signup', views.SignUpView.as_view()),
    #d signin
    path('signin', views.SignInView.as_view()),
    #d user
    path('users/<int:userid>', views.UserView.as_view()),
    #d alluser
    path('users', views.AllUsersView.as_view()),
    #d task, updatetask, deletetask
    path('tasks/<int:taskid>', views.TaskView.as_view()),
    #d alltask, addtask
    path('tasks', views.AllTasksView.as_view()),
    #d userstasks, assign
    path('users/<int:userid>/tasks', views.UsersTasksView.as_view()),
]
