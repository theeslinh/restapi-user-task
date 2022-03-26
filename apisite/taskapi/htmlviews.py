from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.exceptions import NotAuthenticated

from .serializers import UserSerializer, TaskSerializer
from .models import User, Task
import jwt, datetime


def jwt_validate(request):
	token = request.COOKIES.get('jwt')
	if not token:
		raise NotAuthenticated('missing token')
	try:
		payload = jwt.decode(token, 'secret', ['HS256'])
	except jwt.ExpiredSignatureError:
		raise NotAuthenticated('token expired')
	return payload


class SignUpView(APIView):
	renderer_class = [TemplateHTMLRenderer]
	template_name = 'templates/signup.html'

	def get(self, request):
		response = HttpResponse('sign up')
		return response

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		response = HttpResponse('signed up')
		response.data = serializer.data
		return response


class SignInView(APIView):

	def post(self, request):
		name = request.data['name']
		password = request.data['password']
		user = get_object_or_404(User, name=name)
		if not user.check_password(password):
			response = HttpResponse('authentication failed')
			response.data = {
				"error": "wrong password"
			}
		else:
			payload = {
				'id': user.id,
				'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
				'iat': datetime.datetime.utcnow(),
			}

			token = jwt.encode(payload, 'secret', algorithm='HS256')
			
			response = HttpResponse('signed in')
			response.set_cookie(key='jwt', value=token, httponly=True)
		return response


class UserView(generic.DetailView):

	def get(self, request, userid):
		_ = jwt_validate(request)
		user = get_object_or_404(User, id=userid)
		context = {
			'user': user,
		}
		return render(request, 'user/userview.html', context)


class AllUsersView(generic.ListView):
	template_name = 'user/allusersview.html'
	context_object_name = 'all_tasks_list'
	
	def get(self, request):
		_ = jwt_validate(request)
		users = User.objects.all()
		context = {
			'users': users,
		}
		return render(request, 'user/allusersview.html', context)


class AllTasksView(generic.ListView):
	template_name = 'taskapi/allusersview.html'
	context_object_name = 'all_tasks_list'

	def get_queryset(self):
		return Task.objects.all()
	
	def get(self, request):
		_ = jwt_validate(request)
		tasks = Task.objects.all()
		context = {
			'tasks': tasks,
		}
		return render(request, 'taskapi/alltasksview.html', context)

	def post(self, request):
		_ = jwt_validate(request)
		serializer = TaskSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return HttpResponse(serializer.data)


class TaskView(generic.DetailView):

	def get(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		context = {
			'task': task,
		}
		return render(request, 'user/taskview.html', context)
		
	def patch(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		if task.status == 'C':
			response = HttpResponse('task completed')
			response.data = {
				"error": "cannot update completed task"
			}
		else:
			serializer = TaskSerializer(task, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			response = HttpResponse('task updated')
			response.data = serializer.data
		return response

	def delete(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		if task.status == 'C':
			response = HttpResponse('task completed')
			response.data = {
				"error": "cannot delete completed task"
			}
		else:
			serializer = TaskSerializer(task)
			response = HttpResponse('task deleted')
			response.data = serializer.data
			task.delete()
		return response


class UsersTasksView(generic.ListView):

	def get(self, request, userid):
		_ = jwt_validate(request)
		user = get_object_or_404(User, id=userid)
		tasks = user.task_set.all()
		if not tasks:
			response = HttpResponse('no tasks')
			response.data = {
				"message": "no tasks"
			}
		else:
			response = HttpResponse()
			response.data = list(map(lambda x: TaskSerializer(x).data, tasks))
		return response

	def post(self, request, userid):
		payload = jwt_validate(request)
		user = get_object_or_404(User, id=userid)
		if payload['id'] == userid:
			response = HttpResponse('assigning failed')
			response.data = {
				"error": "cannot assign a task to yourself"
			}
		else:
			task = get_object_or_404(Task, id=request.data['taskid'])
			if task.user_id == user:
				response = HttpResponse('assigning failed')
				response.data = {
					"error": "user was already assigned this task"
				}
			else:
				task.user_id = user
				task.save()
				response = HttpResponse('assigning success')
				response.data = TaskSerializer(task).data
		return response
