## serializers.py

from rest_framework import serializers
from .models import User, Profile, Match, Message, Project, Task

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'skills', 'interests', 'bio']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = Profile.objects.update_or_create(user=user, **validated_data)
        return profile

class MatchSerializer(serializers.ModelSerializer):
    """Serializer for the Match model."""
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'score']

    def create(self, validated_data):
        user1_data = validated_data.pop('user1')
        user2_data = validated_data.pop('user2')
        user1 = UserSerializer.create(UserSerializer(), validated_data=user1_data)
        user2 = UserSerializer.create(UserSerializer(), validated_data=user2_data)
        match, created = Match.objects.update_or_create(user1=user1, user2=user2, **validated_data)
        return match

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']

    def create(self, validated_data):
        sender_data = validated_data.pop('sender')
        receiver_data = validated_data.pop('receiver')
        sender = UserSerializer.create(UserSerializer(), validated_data=sender_data)
        receiver = UserSerializer.create(UserSerializer(), validated_data=receiver_data)
        message, created = Message.objects.update_or_create(sender=sender, receiver=receiver, **validated_data)
        return message

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    assigned_to = UserSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assigned_to', 'due_date', 'status', 'project']

    def create(self, validated_data):
        assigned_to_data = validated_data.pop('assigned_to')
        assigned_to = UserSerializer.create(UserSerializer(), validated_data=assigned_to_data)
        task, created = Task.objects.update_or_create(assigned_to=assigned_to, **validated_data)
        return task

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the Project model."""
    members = UserSerializer(many=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'members', 'tasks']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        project = Project.objects.create(**validated_data)
        for member_data in members_data:
            member = UserSerializer.create(UserSerializer(), validated_data=member_data)
            project.members.add(member)
        return project
