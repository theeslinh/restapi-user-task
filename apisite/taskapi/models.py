from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class User(AbstractUser):
	id = models.BigAutoField(primary_key=True, editable=False)
	name = models.CharField(max_length=16, blank=False, null=False)
	password = models.CharField(max_length=16, blank=False, null=False)
	username = None

	USERNAME_FIELD = 'id'
	REQUIRED_FIELD = []

	def __str__(self):
		return self.name


class Task(models.Model):

	class TaskStatus(models.TextChoices):
		NEW = 'NEW'
		COMPLETE = 'COMPLETE'

	id = models.BigAutoField(primary_key=True, editable=False)
	name = models.CharField(max_length=16, blank=False, null=False)
	descr = models.CharField(verbose_name='task description', max_length=255)
	user_id = models.ForeignKey(User, to_field='id', verbose_name='assigned user id', on_delete=models.SET_NULL, blank=False, null=True)
	due = models.DateTimeField(verbose_name='date of completion', blank=False)
	status = models.CharField(max_length=8, choices=TaskStatus.choices, default=TaskStatus.NEW)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
