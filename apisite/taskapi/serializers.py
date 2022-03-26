from rest_framework import serializers
from .models import User, Task
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'name', 'password']
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance


class TaskSerializer(serializers.ModelSerializer):

	class Meta:
		model = Task
		fields = ['id', 'name', 'descr', 'user_id',
				'due', 'status', 'created', 'modified']
		extra_kwargs = {
			'id': {'read_only': True},
			'created': {'read_only': True},
			'modified': {'read_only': True},
		}

	def create(self, validated_data):
		instance = self.Meta.model(**validated_data)
		instance.save()
		return instance

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance

	def delete(self, validated_data):
		instance = self.Meta.model(**validated_data)
