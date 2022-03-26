from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotAuthenticated, ParseError

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

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		response = Response('signed up')
		response.data = serializer.data
		return response


class SignInView(APIView):

	def post(self, request):
		try:
			id = request.data['id']
			password = request.data['password']
		except KeyError:
			raise ParseError("invalid json format: 'id' and 'password' are required")
		user = get_object_or_404(User, id=id)
		if not user.check_password(password):
			response = Response('authentication failed')
			response.status_code = 401
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
			
			response = Response('signed in')
			response.set_cookie(key='jwt', value=token, httponly=True)
			response.data = {
				"message": "signed in",
			}
		return response


class UserView(APIView):

	def get(self, request, userid):
		_ = jwt_validate(request)
		user = get_object_or_404(User, id=userid)

		if user is None:
			response = Response('user not found')
			response.data = {
				"error": "user not found"
			}
		else:
			serializer = UserSerializer(user)
			response = Response('user found')
			response.data = serializer.data
		return response


class AllUsersView(APIView):
	def get(self, request):
		_ = jwt_validate(request)
		users = User.objects.all()
		if not users:
			response = Response('no users')
			response.data = {
				"message": "no users"
			}
		else:
			response = Response()
			response.data = list(map(lambda x: UserSerializer(x).data, users))
		return response


class AllTasksView(APIView):
	def get(self, request):
		_ = jwt_validate(request)
		tasks = Task.objects.all()
		if not tasks:
			response = Response('no tasks')
			response.data = {
				"message": "no tasks"
			}
		else:
			response = Response()
			response.data = list(map(lambda x: TaskSerializer(x).data, tasks))
		return response

	def post(self, request):
		_ = jwt_validate(request)
		serializer = TaskSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class TaskView(APIView):

	def get(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		serializer = TaskSerializer(task)
		response = Response('task found')
		response.data = serializer.data
		return response

	def patch(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		if task.status == 'C':
			response = Response('task completed')
			response.data = {
				"error": "cannot update completed task"
			}
		else:
			serializer = TaskSerializer(task, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			response = Response('task updated')
			response.data = serializer.data
		return response

	def delete(self, request, taskid):
		_ = jwt_validate(request)
		task = get_object_or_404(Task, id=taskid)
		if task.status == 'C':
			response = Response('task completed')
			response.data = {
				"error": "cannot delete completed task"
			}
		else:
			serializer = TaskSerializer(task)
			response = Response('task deleted')
			response.data = serializer.data
			task.delete()
		return response


class UsersTasksView(APIView):

	def get(self, request, userid):
		_ = jwt_validate(request)
		user = get_object_or_404(User, id=userid)
		tasks = user.task_set.all()
		if not tasks:
			response = Response('no tasks')
			response.data = {
				"message": "no tasks"
			}
		else:
			response = Response()
			response.data = list(map(lambda x: TaskSerializer(x).data, tasks))
		return response

	def post(self, request, userid):
		payload = jwt_validate(request)
		user = get_object_or_404(User, id=userid)
		if payload['id'] == userid:
			response = Response('assigning failed')
			response.data = {
				"error": "cannot assign a task to yourself"
			}
		else:
			task = get_object_or_404(Task, id=request.data['taskid'])
			if task.user_id == user:
				response = Response('assigning failed')
				response.data = {
					"error": "user was already assigned this task"
				}
			else:
				task.user_id = user
				task.save()
				response = Response('assigning success')
				response.data = TaskSerializer(task).data
		return response
