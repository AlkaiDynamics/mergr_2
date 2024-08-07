## views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Profile, Match, Message, Project, Task
from .serializers import (
    UserSerializer, ProfileSerializer, MatchSerializer, 
    MessageSerializer, ProjectSerializer, TaskSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing User instances."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Profile instances."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class MatchViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Match instances."""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['get'])
    def find_matches(self, request):
        user = request.user
        # Implement your matching logic here
        matches = Match.objects.filter(user1=user)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Message instances."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver')
        content = request.data.get('content')
        receiver = get_object_or_404(User, id=receiver_id)
        message = Message(sender=sender, receiver=receiver, content=content)
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Project instances."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        project.members.add(user)
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Task instances."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['post'])
    def assign_task(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        task.assigned_to = user
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)
